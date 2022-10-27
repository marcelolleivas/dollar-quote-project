import requests

from dollar_quote.exceptions import ServiceStatusException

BASE_URL = "https://api.vatcomply.com"
RATE_ENDPOINT = "rates"


class VATService(object):
    def __init__(self):
        self.base_url = BASE_URL

    def get_rate(self, date, base="USD"):
        params = {
            "date": date,
            "base": base,
        }
        endpoint = f"{self.base_url}/{RATE_ENDPOINT}"
        response = requests.get(url=endpoint, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise ServiceStatusException

        return response.json()
