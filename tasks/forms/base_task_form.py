from django import forms

from common.validators import ValidateDate
from users.models import User


class BaseTaskForm(forms.ModelForm):
    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        if self.request and self.request.user.is_authenticated:
            self.fields['assignee'].queryset = User.objects.filter(company=self.request.user.company)

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        validator = ValidateDate(field_names=["deadline"], days=365, future=None, form=self)
        validator(deadline)
        return deadline
