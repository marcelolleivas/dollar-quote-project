from rest_framework import serializers

from dollar_quote.rates.models import Rate


class RateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rate
        fields = ["date", "brazilian_real", "euro", "japanese_yen"]
