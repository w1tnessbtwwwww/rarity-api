from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenFromIDProvider(BaseModel):
    token: str


class TokenCreate(BaseModel):
    user_id: UUID
    token: str
    token_type: str


class TokenRead(BaseModel):
    user_id: UUID
    token: str
    created_at: datetime
