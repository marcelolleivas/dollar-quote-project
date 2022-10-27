from rest_framework import mixins, viewsets

from dollar_quote.rates.models import Rate
from dollar_quote.rates.serializers import RateSerializer


class RateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all().order_by("-date")

    def get_queryset(self, *args, **kwargs):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            self.queryset = Rate.objects.filter(
                date__range=[start_date, end_date]
            ).order_by("-date")
        return self.queryset
