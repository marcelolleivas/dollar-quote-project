from datetime import datetime

from django.shortcuts import render

from dollar_quote.rates.models import Rate
from dollar_quote.rates.utils import get_workdays


def index(request):
    # default values
    error = None
    data = None

    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    # check if user has sent the values
    if date_start and date_end:
        date_start = datetime.strptime(date_start, "%Y-%m-%d")
        date_end = datetime.strptime(date_end, "%Y-%m-%d")

        workdays = get_workdays(date_start, date_end)

        if date_start > date_end or workdays > 5:
            error = (
                "Date start must be less than the end date or "
                "range must be max 5 workdays!"
            )
        else:
            data = Rate.objects.filter(date__range=[date_start, date_end])
            if not data.exists():
                error = "Database has no data for this date range!"
                data = None

    return render(request, "rates/home.html", {"error": error, "data": data})
