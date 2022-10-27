FROM python:3.10.0-alpine

RUN mkdir /dollar_quote
WORKDIR /dollar_quote


ENV \
    PYTHONUNBUFFERED=1 \
    CELERY_BEAT_MAX_LOOP_INTERVAL=5 \
    QUEUE_TTL_MINUTES=0 \
    EXCHANGE_NO_DECLARE=1

COPY . /dollar_quote

RUN python -m pip install --upgrade pipenv wheel
RUN pipenv install --system --deploy --ignore-pipfile
