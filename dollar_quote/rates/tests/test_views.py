import pytest

from dollar_quote.rates.models import Rate


class TestRateIndex:

    endpoint = "/rates"

    @pytest.mark.parametrize(
        "date_start,date_end,currency",
        [
            ["2022-10-24", "2022-10-24", "0"],
            ["2022-10-24", "2022-10-25", "1"],
            ["2022-10-24", "2022-10-26", "2"],
            ["2022-10-24", "2022-10-27", "0"],
            ["2022-10-24", "2022-10-28", "1"],
            ["2022-10-24", "2022-10-29", "2"],
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

        # ARRANGE
        assert response.status_code == 200

    def test_valid_params_multiple_data_succeeds(self, client, multiple_rates):
        # ARRANGE
        Rate.objects.all().update(date="2022-10-24")

        # ACT
        params = {
            "date_start": "2022-10-24",
            "date_end": "2022-10-25",
            "currency_options": "0",
        }
        response = client.post(self.endpoint, data=params)

        # ARRANGE
        assert response.status_code == 200

    def test_wrong_date_end_get_error(self):
        ...

    def test_date_start_greater_than_end_get_error(self):
        ...

    def test_date_range_workdays_greater_than_five_get_error(self):
        ...

    def test_database_returned_empty_get_error(self):
        ...
