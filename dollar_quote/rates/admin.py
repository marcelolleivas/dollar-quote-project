from django.contrib import admin

from dollar_quote.rates.models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    ...
