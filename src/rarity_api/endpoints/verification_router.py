from fastapi import APIRouter, Depends

from rarity_api.common.auth.native_auth.dependencies import authenticate
from rarity_api.common.auth.schemas.user import UserRead

router = APIRouter(
    prefix="/verification",
    tags=["verification"]
)


@router.post("/resend")
async def resend_verification_email(user: UserRead = Depends(authenticate)):
    return

@router.post("/verify")
async def verify_email(user):
    return