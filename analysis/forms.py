from django import forms
from django.utils.translation import gettext_lazy as _

from common.validators import ValidateDate
from .models import PERIOD_CHOICES
from .services.analysis_generator import AnalysisGenerator


class GenerationForm(forms.Form):
    start_date = forms.DateTimeField(
        label=_('Select date'),
        validators=[ValidateDate(field_names=["start_date"], days=120, future=False)]
    )
    end_date = forms.DateTimeField()
    period = forms.TypedChoiceField(
        choices=PERIOD_CHOICES,
        coerce=int
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        self._service = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        period = cleaned_data.get('period')

        if not (start_date and end_date and period):
            return cleaned_data
        service = AnalysisGenerator(
            user=self.user,
            start_date=start_date.date(),
            end_date=end_date.date(),
            period=period)
        try:
            service.validate()
        except ValueError as e:
            self.add_error(None, str(e))
        else:
            self._service = service

        return cleaned_data

    def save(self):
        if not self._service:
            raise RuntimeError("Cannot save: validation did not run or failed.")
        return self._service.generate()
