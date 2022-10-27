import datetime
import decimal

from django.core.exceptions import ValidationError
from django.utils import timezone

import pytest

from dollar_quote.rates.utils import json_serial, present_or_past_data


class TestUtils:
    # ARRANGE
    @pytest.mark.parametrize(
        "obj, obj_serial_type",
        [
            [timezone.now(), str],
            [decimal.Decimal("1.27"), float],
        ],
    )
    def test_json_serial(self, obj, obj_serial_type):
        # ACT
        data = json_serial(obj)

        # ASSERT
        assert isinstance(data, obj_serial_type)

    # ARRANGE
    @pytest.mark.parametrize(
        "value",
        [
            timezone.now() + datetime.timedelta(days=10),
        ],
    )
    def test_present_or_past_data(self, value):
        value = value.date()

        # ASSERT
        with pytest.raises(ValidationError):
            present_or_past_data(value)
