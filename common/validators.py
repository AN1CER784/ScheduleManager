from django.core.exceptions import ValidationError

from common.utils import is_meaningful

class ValidateText:
    def __init__(self, field_name='text'):
        self.field_name = field_name

    def __call__(self, value):
        if not is_meaningful(value):
            raise ValidationError(f'{self.field_name.capitalize()} must be in English or Russian; Give more understandable {self.field_name}')