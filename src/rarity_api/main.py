from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from sqladmin import Admin

from .common.auth.yandex_auth.router import router as yandex_router
from .admin.user_admin import UserAdmin
from .common.http_client import HttpClient
from .core.database.connector import get_engine_sync
from .endpoints.city_router import router as city_router
from .endpoints.country_router import router as country_router
from .endpoints.item_router import router as item_router
from .endpoints.manufacturer_router import router as manufacturer_router
from .endpoints.region_router import router as region_router
from .endpoints.search_history_router import router as search_history_router
from .common.auth.google_auth.router import router as google_auth_router
from .common.auth.google_auth.utils.id_provider_certs import IdentityProviderCerts
from .common.auth.native_auth.router import router as plain_auth_router
from .endpoints.user_router import router as user_router
from .endpoints.payment_router import router as payment_router

app = FastAPI(
    title="Rarity API",
    description="API for managing porcelain rarity data",
    version="1.0.0"
)

app.include_router(google_auth_router)
app.include_router(plain_auth_router)
# Include all routers
app.include_router(country_router)
app.include_router(region_router)
app.include_router(city_router)
app.include_router(manufacturer_router)
app.include_router(item_router)
app.include_router(search_history_router)
app.include_router(yandex_router)
app.include_router(user_router)
app.include_router(payment_router)

admin = Admin(app, get_engine_sync())
admin.add_view(UserAdmin)

@asynccontextmanager
async def lifespan():
    http_client = HttpClient()
    await http_client.init_session()
    await IdentityProviderCerts().renew_certs()
    run_migrations()
    yield
    await http_client.close_session()


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
