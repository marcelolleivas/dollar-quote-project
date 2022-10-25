from django.utils import timezone

from config.celery import app
from dollar_quote.rates.models import Rate
from dollar_quote.services import VATService

service = VATService()


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 300},
)
def populate_database(self):
    date = timezone.now()
    data = service.get_rate(date)
    try:
        Rate.objects.create(
            date=date,
            brazilian_real=data["rates"]["BRL"],
            euro=data["rates"]["EUR"],
            japanese_yen=data["rates"]["JPY"],
        )
    except KeyError:
        # TODO: ...
        ...
