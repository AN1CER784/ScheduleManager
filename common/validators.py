from django.core.exceptions import ValidationError
from django.utils import timezone


class ValidateDate:
    def __init__(self, field_names=None, days=60, future=None, form=None):
        self.field_names = field_names if isinstance(field_names, list) else ['Date']
        self.days = days
        self.min_date = timezone.now() - timezone.timedelta(days=days)
        self.max_date = timezone.now() + timezone.timedelta(days=days)
        self.future = future
        self.errors = []
        self.form = form

    def __call__(self, value):
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

    def _validate_future_or_none(self, value):
        if not (self.min_date <= value <= self.max_date):
            for field_name in self.field_names:
                self.errors.append(f"{field_name} must be within {self.days} days")

    def _validate_future(self, value, now):
        if value < now:
            for field_name in self.field_names:
                self.errors.append(f"{field_name} must be in the future")

    def _validate_past(self, value, now):
        if value > now:
            for field_name in self.field_names:
                self.errors.append(f"{field_name} must be in the past")
        if value < self.min_date:
            for field_name in self.field_names:
                self.errors.append(f"{field_name} must be within {self.days} days")

    def _add_errors(self):
        for error, field_name in zip(self.errors, self.field_names):
            if self.form:
                self.form.add_error(field_name, error)
            else:
                raise ValidationError(error)

