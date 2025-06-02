from fastapi import APIRouter, Depends, Request

from rarity_api.common.auth.native_auth.dependencies import authenticate
from rarity_api.common.auth.schemas.user import UserRead


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/subcription", summary="Получить подписку пользователя")
async def get_user_subscription(request: Request, user: UserRead = Depends(authenticate)):
    return user