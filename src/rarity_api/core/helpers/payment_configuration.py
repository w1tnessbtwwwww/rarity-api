from yookassa import Configuration
from rarity_api.settings import settings


class PaymentConfiguration():
    def __init__(self):
        yookassa_configuration = Configuration()
        yookassa_configuration.account_id = settings.yookassa_shop_id
        yookassa_configuration.secret_key = settings.yookassa_secret_key

        self.yookassa_configuration = yookassa_configuration

