from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from rarity_api.common.auth.native_auth.dependencies import authenticate
from rarity_api.common.auth.schemas.user import UserRead
from rarity_api.core.database.connector import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from rarity_api.core.database.models.models import User
from rarity_api.core.database.repos.repos import UserRepository
router = APIRouter(
    prefix="/verification",
    tags=["verification"]
)


@router.post("/resend")
async def resend_verification_email(user: UserRead = Depends(authenticate)):
    return

@router.post("/verify")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    usr: User = UserRepository(session).get_one_by_filter(verify_token=token)
    if usr is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    if usr.token_expires < datetime.now(tz=datetime.timezone.utc):
        raise HTTPException(
            status_code=401,
            detail="Verification token expired"
        )
    
    await UserRepository(session).verify_user(usr.id)
    return {
        "verify": True
    }
    