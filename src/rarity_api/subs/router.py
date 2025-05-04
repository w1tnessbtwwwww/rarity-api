import uuid

import stripe
from fastapi import APIRouter, Depends
from rarity_api.common.auth.dependencies import authenticate
from rarity_api.common.auth.exceptions import AuthException
from rarity_api.common.auth.repositories.user_repository import UserRepository
from rarity_api.common.auth.schemas.user import UserRead, UserSub, Fullname
from rarity_api.common.logger import logger
from rarity_api.database import get_session
from rarity_api.settings import settings
from rarity_api.subs.schemas import CreateSubscriptionData, SubscriptionData
from rarity_api.subs.subscription_repository import SubscriptionRepository
from rarity_api.subs.tochka_client import TochkaClient
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from stripe import PaymentLink

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/profile")
async def auth_user_check_self_info(
        user: UserRead = Depends(authenticate),
        session=Depends(get_session)
):
    by_user = await SubscriptionRepository(session).find_by_user(user.id)
    sub = UserSub(id=user.id, email=user.email, created_at=user.created_at,
                  first_name=user.first_name, second_name=user.second_name, last_name=user.last_name,
                  is_verified=user.is_verified,
                  subscription=SubscriptionData(id=by_user.id, status=by_user.status,
                                                expiration_date=by_user.expiration_date,
                                                provider=by_user.provider))
    return sub


@router.get("/logged-in")
async def auth_user_check_self_info(
        request: Request,
        response: Response,
        session=Depends(get_session)
):
    try:
        await authenticate(request, response, session)
        return True
    except AuthException as e:
        logger.error(e)
        return False


@router.put("/profile/fullname")
async def change_user_fullname(
        fullname_data: Fullname,
        user: UserRead = Depends(authenticate),
        session=Depends(get_session)
):
    repo = UserRepository(session=session)
    upd = await repo.update_one(user.id, fullname_data)
    return UserRead.model_validate(upd)


@router.get("/subscription")
async def get_sub(
        user: UserRead = Depends(authenticate),
        session=Depends(get_session)
) -> SubscriptionData:
    by_user = await SubscriptionRepository(session).find_by_user(user.id)
    return SubscriptionData(id=by_user.id, status=by_user.status,
                            expiration_date=by_user.expiration_date,
                            provider=by_user.provider)


# https://docs.stripe.com/payment-links/api
stripe.api_key = settings.stripe_api_key


@router.post("/subscription")
async def activate_subscription(
        data: CreateSubscriptionData,
        user: UserRead = Depends(authenticate)
):
    if data.country_code == 'en':
        mid = settings.stripe_monthly_pricing_id
        yid = settings.stripe_yearly_pricing_id
        url = settings.api_base_url + '/api/users/subscription/stripe/callback?client_reference_id=' + user.id.__str__()
        payment_link = PaymentLink.create(
            line_items=[{'price': mid if data.period == 'MONTHLY' else yid, 'quantity': 1}],
            after_completion=PaymentLink.CreateParamsAfterCompletion(
                type="redirect", redirect=PaymentLink.CreateParamsAfterCompletionRedirect(url=url)
            )
        )
        print(payment_link)
        # todo: save invoice id from response and then update it's status – successful or not
        return payment_link.url
    else:
        redir = settings.api_base_url + '/api/users/subscription/tochka/callback?client_reference_id=' + user.id.__str__()
        client = TochkaClient(api_token=settings.tochka_api_token, customer_code=settings.tochka_customer_code,
                              base_redirect_url=redir)
        data = await client.send_request('9900' if data.period == 'MONTHLY' else '99000', uuid.uuid4().__str__())
        return data['paymentLink']


@router.get("/subscription/stripe/callback")
async def stripe_callback(
        client_reference_id: str,
        session=Depends(get_session)
):
    uri = settings.post_login_redirect_uri + '?success=true'
    repository = SubscriptionRepository(session=session)
    sub = await repository.find_by_user(uuid.UUID(client_reference_id))
    sub.status = "Active"
    await repository.update(sub)
    return RedirectResponse(url=uri)


@router.get("/subscription/tochka/callback")
async def tochka_callback(
        client_reference_id: str,
        session=Depends(get_session)
):
    uri = settings.post_login_redirect_uri + '?success=true'
    repository = SubscriptionRepository(session=session)
    sub = await repository.find_by_user(uuid.UUID(client_reference_id))
    sub.status = "Active"
    await repository.update(sub)
    return RedirectResponse(url=uri)

# and callbacks ...
