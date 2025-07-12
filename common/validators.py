from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _


class ValidateDate:
    def __init__(self, field_names: list[str] | None = None, days: int = 60, future: bool = None,
                 form: forms.Form = None):
        self.field_names = field_names if isinstance(field_names, list) else ['Date']
        self.days = days
        self.future = future
        self.form = form

    def __call__(self, value: datetime.date):
        self.error = None
        self.min_date = timezone.now() - timezone.timedelta(days=self.days)
        self.max_date = timezone.now() + timezone.timedelta(days=self.days)
        now = timezone.now()
        if value is None:
            return
        if self.future:
            self._validate_future(value, now)
            self._validate_future_or_none(value)
        elif self.future is None:
            self._validate_future_or_none(value)
        else:
            self._validate_past(value, now)
        self._add_errors()

    def _validate_future_or_none(self, value: datetime.date) -> None:
        if not (self.min_date <= value <= self.max_date):
            for field_name in self.field_names:
                self.error = (_('%(field)s must be within %(days)s days') % {'field': field_name, 'days': self.days})

    def _validate_future(self, value: datetime.date, now: datetime.date) -> None:
        if value < now:
            for field_name in self.field_names:
                self.error = (_('%(field)s must be in the future') % {'field': field_name})

    def _validate_past(self, value: datetime.date, now: datetime.date) -> None:
        if value > now:
            for field_name in self.field_names:
                self.error = (_('%(field)s must be in the past') % {'field': field_name})
        if value < self.min_date:
            for field_name in self.field_names:
                self.error = (_('%(field)s must be within %(days)s days') % {'field': field_name, 'days': self.days})

    def _add_errors(self) -> None:
        if not self.error:
            return
        if self.form:
            for field_name in self.field_names:
                self.form.add_error(field_name, self.error)
        else:
            raise ValidationError(self.error)
