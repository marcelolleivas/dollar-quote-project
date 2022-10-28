from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError

from dollar_quote.rates.models import Rate
from dollar_quote.rates.serializers import RateSerializer

date_start = OpenApiParameter(
    name="start_date",
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description="Start date to find rates",
)

date_end = OpenApiParameter(
    name="end_date",
    type=OpenApiTypes.DATE,
    location=OpenApiParameter.QUERY,
    description="End date to find rates",
)


@extend_schema(parameters=[date_start, date_end])
class RateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RateSerializer
    queryset = Rate.objects.all().order_by("-date")

    @staticmethod
    def _date_range_is_correct(start, end):
        return start <= end

    def get_queryset(self, *args, **kwargs):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            if not self._date_range_is_correct(start_date, end_date):
                msg = {"detail": "start_date must be less than or equal to end_date"}
                raise ValidationError(msg)
            self.queryset = Rate.objects.filter(
                date__range=[start_date, end_date]
            ).order_by("-date")
        return self.queryset
