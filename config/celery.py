import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("dollar_quote")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.task_default_queue = "celery:1"

app.conf.task_queues = [
    Queue(f"celery:{n}", Exchange(f"celery:{n}"), routing_key=f"celery:{n}")
    for n in range(1, 10)
]

app.conf.beat_schedule = {
    "diary_populate_database": {
        "task": "dollar_quote.rates.tasks.populate_database",
        "schedule": 300,
    }
}

app.conf.timezone = "America/Sao_Paulo"
