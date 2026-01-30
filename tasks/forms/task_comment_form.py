from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from tasks.models import TaskComment


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['task_id', 'text']

    task_id = forms.IntegerField(required=False)
    text = forms.CharField(label='comment', validators=[MinLengthValidator(3), MaxLengthValidator(1000),
                                                        RegexValidator(r'^(?=.*[A-Za-z\u0400-\u04FF]).{3,}$',
                                                                       _('Only english and russian letters are allowed, minimum 3 symbols'))])
