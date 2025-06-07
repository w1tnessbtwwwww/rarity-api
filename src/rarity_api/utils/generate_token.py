import secrets
from datetime import timedelta
import datetime
def generate_confirmation_token():
    return secrets.token_urlsafe(32)

def set_token_expiry():
    return datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(hours=24)  # Токен истекает через 24 часа