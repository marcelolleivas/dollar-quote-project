from datetime import datetime, timedelta


class TestRateApi:

    endpoint = "/api/rates"

    def test_multiple_data_max_ten_succeeded(self, db, client, multiple_rates):
        # ARRANGE

        # ACT
        response = client.get(self.endpoint)

        results = response.json()["results"]

        # ASSERT
        assert response.status_code == 200
        assert len(results) == 10

    def test_with_query_params_succeeded(self, db, client, multiple_rates):
        # ARRANGE
        params = {
            "start_date": (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": (datetime.today()).strftime("%Y-%m-%d"),
        }

        # ACT
        response = client.get(self.endpoint, params=params)

        # ASSERT
        assert response.status_code == 200
