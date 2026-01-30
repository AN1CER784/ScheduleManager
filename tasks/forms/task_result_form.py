from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _

from tasks.models import TaskResult


class TaskResultForm(forms.ModelForm):
    class Meta:
        model = TaskResult
        fields = ['task_id', 'message']

    task_id = forms.IntegerField(required=False)
    message = forms.CharField(label=_("Result message"),
                              validators=[MinLengthValidator(3), MaxLengthValidator(2000)])
