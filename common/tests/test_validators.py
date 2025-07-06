from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from common.validators import ValidateDate


class ValidateDateTestCase(TestCase):
    def test_valid_future_validator(self):
        validator = ValidateDate(field_names=['start_date'], days=60, future=True)
        validator(timezone.now() + timezone.timedelta(days=5))
        self.assertIsNone(validator.error)

    def test_invalid_future_validator(self):
        validator = ValidateDate(field_names=['start_date'], days=60, future=True)
        with self.assertRaises(ValidationError) as context:
            validator(timezone.now() - timezone.timedelta(days=5))
        self.assertIsNotNone(validator.error)
        self.assertIn('start_date must be in the future', context.exception)

    def test_valid_past_validator(self):
        validator = ValidateDate(field_names=['end_date'], days=60, future=False)
        validator(timezone.now() - timezone.timedelta(days=5))
        self.assertIsNone(validator.error)

    def test_invalid_past_validator(self):
        validator = ValidateDate(field_names=['end_date'], days=60, future=False)
        with self.assertRaises(ValidationError) as context:
            validator(timezone.now() + timezone.timedelta(days=5))
        self.assertIsNotNone(validator.error)
        self.assertIn('end_date must be in the past', context.exception)

    def test_valid_future_or_none_validator(self):
        validator = ValidateDate(field_names=['start_date'], days=60, future=None)
        validator(timezone.now() + timezone.timedelta(days=1))
        self.assertIsNone(validator.error)

    def test_invalid_future_or_none_validator(self):
        validator = ValidateDate(field_names=['start_date'], days=60, future=None)
        with self.assertRaises(ValidationError) as context:
            validator(timezone.now() - timezone.timedelta(days=61))
        self.assertIsNotNone(validator.error)
        self.assertIn('start_date must be within 60 days', str(context.exception))
