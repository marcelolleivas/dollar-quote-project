import json

from django.shortcuts import render

from dollar_quote.rates.forms import RateForm
from dollar_quote.rates.utils import json_serial


def index(request):
    context = None

    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            dataset = form.cleaned_data

            category_data_source = {
                "name": f"USD to {dataset['currency'][1]} exchange rate over time",
                "data": [],
            }

            for entry in dataset["data"]:
                data = {
                    "name": json_serial(entry["date"]),
                    "y": json_serial(entry[dataset["currency"][0]]),
                }
                category_data_source["data"].append(data)

            category_chart_data = {
                "chart": {"zoomType": "x"},
                "title": {
                    "text": f"USD to {dataset['currency'][1]} exchange rate over time"
                },
                "xAxis": {"type": "datetime"},
                "yAxis": {"title": {"text": "Exchange rate"}},
                "series": [category_data_source],
            }

            context = json.dumps(category_chart_data)
    else:
        form = RateForm()

    return render(request, "rates/home.html", {"context": context, "form": form})
