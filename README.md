# Dollar Quote Project
Python project to check BRL, EUR, YEN rates compared to USD.

![Actions](https://github.com/marcelolleivas/dollar-quote-project/actions/workflows/pipeline.yml/badge.svg)
![Coverage](docs/coverage.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Installation
Unfortunately Heroku [is not for free anymore](https://techcrunch.com/2022/08/25/heroku-announces-plans-to-eliminate-free-plans-blaming-fraud-and-abuse/)
so here are the options to make yourself ready:

### Docker compose

You can prepare the app locally running:

```
docker-compose up --build
```

### Pipenv

If you are not interested on using Docker run the follow command:

```
make install-dev
```

## Usage
### Populating database
This project has a command where it populates your database with the last 10 days of dollar rating
requesting on [vatcomply](https://www.vatcomply.com/documentation). Please run one of the commands -
depending on which of pipenv or docker-compose you're using.
```
pipenv run python ./manage.py populate_database
```
or
```
docker-compose run web ./manage.py populate_database
```
### Accessing the app
For using the app please run the follow command, if you're not using Docker
(the app is already running on docker if you followed the step on Installation).

```
pipenv run python ./manage.py runserver 0.0.0.0:8000
```

The app will be up on 0.0.0.0:8000.
