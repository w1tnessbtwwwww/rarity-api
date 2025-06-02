from dataclasses import MISSING
from enum import Enum


class PaymentEndpoints(Enum):
    YOOKASSA = "https://api.yookassa.ru/v3/"
    STRIPE = MISSING