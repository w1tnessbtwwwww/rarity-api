import uuid
from datetime import datetime

from pydantic import EmailStr
from rarity_api.database import Base
from sqlalchemy import Boolean, String, UUID, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, nullable=False)
    # all names are nullable at the creation and then set via put
    first_name: Mapped[String] = mapped_column(String(255), nullable=True)
    second_name: Mapped[String] = mapped_column(String(255), nullable=True)
    last_name: Mapped[String] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription = relationship("Subscription", back_populates="user")
    tokens = relationship("Token", back_populates="user")
    auth_credentials = relationship("AuthCredentials", back_populates="user")
