from dataclasses import MISSING
from typing import Dict
import uuid
from fastapi import APIRouter, Depends, HTTPException
from enum import Enum

from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from rarity_api.core.helpers.payment_configuration import PaymentConfiguration
from rarity_api.core.helpers.payment_currencies import PaymentCurrency
from rarity_api.core.helpers.payment_endpoints import PaymentEndpoints
from rarity_api.core.helpers.payment_prices import PaymentPrice
from rarity_api.settings import settings
from rarity_api.common.auth.native_auth.dependencies import authenticate
from rarity_api.common.auth.schemas.user import UserRead

from uuid import uuid4, UUID

from yookassa import Payment, Configuration
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt
from yookassa.domain.models.receipt_data.receipt_item import ReceiptItem
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder

router = APIRouter(
    prefix="/payments",
    tags=["payment"]
)

# class YooKassaAmount(BaseModel):
#     value: str = PaymentPrice.MONTHLY.value
#     currency: str = PaymentCurrency.RUB.value

# class YooKassaRefund(BaseModel):
#     amount: YooKassaAmount
#     payment_id: UUID = uuid.uuid4

Configuration.account_id = settings.yookassa_shop_id
Configuration.secret_key = settings.yookassa_api_key

@router.post("/yookassa/monthly")
async def yookassa_payment(user: UserRead = Depends(authenticate)):
    idempotence_key = str(uuid.uuid4())
    



@router.post("/yookassa/yearly")
async def yookassa_payment(user: UserRead = Depends(authenticate)):
    try:
        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": PaymentPrice.YEARLY.value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://speedsolver.ru"
            },
            "description": "Оплата годовой подписки"
        }, idempotence_key)

        # return RedirectResponse(url=payment.confirmation.confirmation_url)
        return {"payment_id": payment.id, "confirmation_url": payment.confirmation.confirmation_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/yookassa/callback")
async def yookassa_payment_callback():
    ...

@router.post("/stripe")
async def stripe_payment():
    ...

@router.post("/stripe/callback")
async def stripe_payment_callback():
    ...