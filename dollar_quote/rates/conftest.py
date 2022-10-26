import decimal
import random
from datetime import date, timedelta

from django.utils import timezone

import factory
import pytest
from freezegun import freeze_time

from dollar_quote.rates.models import Rate


class RateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rate

    date = factory.LazyFunction(date.today().isoformat)
    brazilian_real = decimal.Decimal("5.30")
    euro = decimal.Decimal("0.99")
    japanese_yen = decimal.Decimal("146.37")


@pytest.fixture
def client():
    from django.test.client import Client

    return Client()


@pytest.fixture
@freeze_time("2022-10-20")
def rate(db):
    return RateFactory.create()


@pytest.fixture
@freeze_time("2022-10-20")
def multiple_rates(db):
    for i in range(10):
        days = i
        brazilian_real = decimal.Decimal(random.randrange(4, 5))
        euro = decimal.Decimal(random.randrange(1, 3))
        japanese_yen = decimal.Decimal(random.randrange(130, 150))
        date = timezone.now() - timedelta(days=days)
        RateFactory.create(
            date=date,
            brazilian_real=brazilian_real,
            euro=euro,
            japanese_yen=japanese_yen,
        )
