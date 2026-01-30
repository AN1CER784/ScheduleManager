from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from tasks.forms.base_task_form import BaseTaskForm
from tasks.models import Task
from users.models import User


class TaskUpdateForm(BaseTaskForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assignee', 'priority', 'deadline']

    name = forms.CharField(label=_('Write task title'),
                           validators=[MinLengthValidator(3), MaxLengthValidator(100),
                                       RegexValidator(r'^(?=.*[A-Za-z\u0400-\u04FF]).{3,}$',
                                                      _('Only english and russian letters are allowed, minimum 3 symbols'))])
    description = forms.CharField(label=_('Write description'), required=False,
                                  validators=[MinLengthValidator(3), MaxLengthValidator(1000),
                                              RegexValidator(r'^(?=.*[A-Za-z\u0400-\u04FF]).{3,}$',
                                                             _('Only english and russian letters are allowed, minimum 3 symbols'))])
    assignee = forms.ModelChoiceField(label=_("Assignee"), queryset=User.objects.none())
    priority = forms.ChoiceField(label=_("Priority"), choices=Task.Priority.choices)
    deadline = forms.DateTimeField(label=_("Deadline"), required=False,
                                   input_formats=['%Y-%m-%dT%H:%M'],
                                   widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
