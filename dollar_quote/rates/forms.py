from django import forms
from django.core.exceptions import BadRequest

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from dollar_quote.rates.models import Rate
from dollar_quote.rates.utils import get_workdays, present_or_past_data


class RateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "rate_form_id"
        self.helper.form_class = "rate_form"
        self.helper.form_action = "submit_survey"

        self.helper.add_input(Submit("submit", "Submit"))

    currency_options = forms.ChoiceField(
        label="Which currency you choose?",
        choices=(
            (0, " Brazilian Real (BRL)"),
            (1, " Euro (EUR)"),
            (2, " Japenese Yen (YEN)"),
        ),
        widget=forms.RadioSelect,
        initial="0",
        required=True,
    )

    date_start = forms.DateField(
        label="Start date:",
        widget=forms.DateInput(attrs=dict(type="date")),  # noqa: C408
        required=True,
    )

    date_end = forms.DateField(
        label="End date:",
        widget=forms.DateInput(attrs=dict(type="date")),  # noqa: C408
        validators=[present_or_past_data],
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()

        currency_chosen = {
            "0": ("brazilian_real", "BRL"),
            "1": ("euro", "EUR"),
            "2": ("japanese_yen", "YEN"),
        }[cleaned_data["currency_options"]]

        date_start = cleaned_data.get("date_start")
        date_end = cleaned_data.get("date_end")

        # confirms present_or_past_data validator
        if not date_end:
            msg = "End date must be till today"
            raise BadRequest(msg)

        workdays = get_workdays(date_start, date_end)

        if date_start > date_end or workdays > 5:
            msg = (
                "Date start must be less than the end date or "
                "range must be max 5 workdays!"
            )
            raise BadRequest(msg)
        else:
            dataset = (
                Rate.objects.filter(date__range=[date_start, date_end])
                .values("date", currency_chosen[0])
                .order_by("date")
            )
            if not dataset.exists():
                msg = "Database has no data for this date range!"
                raise forms.ValidationError(msg)
            return {"data": dataset, "currency": currency_chosen}
