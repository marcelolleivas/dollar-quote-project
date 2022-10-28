from datetime import datetime, timedelta

from django.core.management import BaseCommand
from django.db import IntegrityError

from dollar_quote.rates.models import Rate
from dollar_quote.services import VATService


class Command(BaseCommand):  # pragma: no cover
    def handle(self, *args, **options):
        service = VATService()
        days = 10
        data_to_db = []
        for i in range(days):
            date = datetime.today() - timedelta(days=i)
            date = date.strftime("%Y-%m-%d")
            service_data = service.get_rate(date)
            data_to_db.append(
                Rate(
                    date=date,
                    brazilian_real=service_data["rates"]["BRL"],
                    euro=service_data["rates"]["EUR"],
                    japanese_yen=service_data["rates"]["JPY"],
                )
            )
        try:
            Rate.objects.bulk_create(data_to_db)
        except IntegrityError:
            return
