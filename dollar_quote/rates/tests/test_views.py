import datetime

from django.utils import timezone

import pytest

from dollar_quote.rates.models import Rate


class TestRateIndex:

    endpoint = "/rates"

    @pytest.mark.parametrize(
        "date_start,date_end,currency",
        [
            ["2022-10-17", "2022-10-17", "0"],
            ["2022-10-17", "2022-10-18", "1"],
            ["2022-10-17", "2022-10-19", "2"],
            ["2022-10-17", "2022-10-20", "0"],
            ["2022-10-17", "2022-10-21", "1"],
            ["2022-10-07", "2022-10-13", "0"],
        ],
    )
    def test_valid_params_unique_data_succeeds(
        self, date_start, date_end, currency, client, rate
    ):
        # ARRANGE
        rate.date = "2022-10-24"
        rate.save(force_update=True)

        # ACT
        params = {
            "date_start": date_start,
            "date_end": date_end,
            "currency_options": currency,
        }
        response = client.post(self.endpoint, data=params)

        # ASSERT
        assert response.status_code == 200

    def test_valid_params_multiple_data_succeeds(self, client, multiple_rates):
        # ARRANGE
        Rate.objects.all().update(date="2022-10-24")

        params = {
            "date_start": "2022-10-24",
            "date_end": "2022-10-25",
            "currency_options": "0",
        }

        # ACT
        response = client.post(self.endpoint, data=params)

        # ASSERT
        assert response.status_code == 200

    def test_database_returned_empty_succeeds(self, db, client):
        # ARRANGE
        params = {
            "date_start": "2022-10-24",
            "date_end": "2022-10-25",
            "currency_options": "0",
        }

        # ACT
        response = client.post(self.endpoint, data=params)

        # ASSERT
        assert response.status_code == 200

    def test_end_date_tomorrow_and_get_error(self, client, multiple_rates):
        # ARRANGE
        params = {
            "date_start": "2022-10-24",
            "date_end": timezone.now() + datetime.timedelta(days=1),
            "currency_options": "1",
        }

        # ACT
        response = client.post(self.endpoint, data=params)

        # ASSERT
        assert response.status_code == 400

    def test_date_start_greater_than_end_get_error(self, client, multiple_rates):
        # ARRANGE
        params = {
            "date_start": "2022-10-25",
            "date_end": "2022-10-24",
            "currency_options": "1",
        }

        # ACT
        response = client.post(self.endpoint, data=params)

        # ASSERT
        assert response.status_code == 400

    def test_date_range_workdays_greater_than_five_get_error(
        self, client, multiple_rates
    ):
        # ARRANGE
        params = {
            "date_start": "2022-10-07",
            "date_end": "2022-10-17",
            "currency_options": "1",
        }

        # ACT
        response = client.post(self.endpoint, data=params)

        # ASSERT
        assert response.status_code == 400
