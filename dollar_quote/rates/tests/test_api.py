import decimal
import random
from datetime import datetime, timedelta

from django.utils import timezone

import freezegun

from dollar_quote.rates.models import Rate


class TestRateApi:

    endpoint = "/api/rates/"

    def test_multiple_data_max_ten_succeeded(self, db, client, multiple_rates):
        # ARRANGE

        # ACT
        response = client.get(f"{self.endpoint}")

        # ASSERT
        assert response.status_code == 200
        assert len(response.json()["results"]) == 10

    def test_multiple_second_page_succeeded(self, db, client, multiple_rates):
        # ARRANGE
        brazilian_real = decimal.Decimal(random.randrange(4, 5))
        euro = decimal.Decimal(random.randrange(1, 3))
        japanese_yen = decimal.Decimal(random.randrange(130, 150))

        Rate.objects.create(
            date=timezone.now() + timedelta(days=1),
            brazilian_real=brazilian_real,
            euro=euro,
            japanese_yen=japanese_yen,
        )

        # ACT
        response = client.get(f"{self.endpoint}?page=2")

        # ASSERT
        assert response.status_code == 200
        assert len(response.json()["results"]) == 1

    @freezegun.freeze_time("2022-10-20")
    def test_with_query_params_succeeded(self, db, client, multiple_rates):
        # ARRANGE
        params = {
            "start_date": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": (datetime.today()).strftime("%Y-%m-%d"),
        }

        # ACT
        response = client.get(self.endpoint, params)

        # ASSERT
        assert response.status_code == 200
        assert len(response.json()["results"]) == 3
