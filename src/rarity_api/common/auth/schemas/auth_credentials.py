from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class AuthCredentialsCreate(BaseModel):
    user_id: UUID
    auth_type: str
    password_hash: Optional[bytes] = None


class AuthCredentialsRead(AuthCredentialsCreate):
    id: UUID
