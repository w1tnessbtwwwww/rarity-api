from rarity_api.common.auth.models.auth_credentials import AuthCredentials
from rarity_api.common.auth.schemas.auth_credentials import AuthCredentialsCreate
from rarity_api.database import AbstractRepository


class AuthCredentialsRepository(AbstractRepository):
    model = AuthCredentials

    async def get_or_create(self, auth_data: AuthCredentialsCreate):
        existing_auth_data = await self.get_by_filter({"user_id": auth_data.user_id})

        if existing_auth_data:
            return existing_auth_data[0]
        else:
            created_auth_data = await self.create(auth_data)
            return created_auth_data
