from django.shortcuts import render

from dollar_quote.rates.forms import RateForm
from dollar_quote.rates.utils import json_serial


def index(request):
    context = None

    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            dataset = form.cleaned_data
            currency = dataset["currency"][1]
            categories = []
            series = [{"name": currency, "data": []}]

            for entry in dataset["data"]:
                categories.append(json_serial(entry["date"]))
                series[0]["data"].append(json_serial(entry[dataset["currency"][0]]))

            context = {"currency": currency, "categories": categories, "series": series}
    else:
        form = RateForm()

    return render(request, "rates/home.html", {"context": context, "form": form})
