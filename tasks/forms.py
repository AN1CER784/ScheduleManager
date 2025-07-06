from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from common.validators import ValidateDate
from tasks.models import Task, TaskComment
from tasks.utils import combine_date_and_time


class BaseTaskForm(forms.ModelForm):
    def clean(self, start_datetime=None, due_datetime=None, update=False):
        cleaned_data = super().clean()
        if start_datetime and due_datetime:
            if due_datetime < start_datetime:
                if not update:
                    fields = ['due_date', 'due_time', ]
                else:
                    fields = ['due_datetime']
                for field in fields:
                    self.add_error(field, _('Due date and time must be after start date and time'))
        return cleaned_data


class TaskCreateForm(BaseTaskForm):
    class Meta:
        model = Task
        fields = ['start_date', 'start_time', 'due_date', 'due_time', 'name', 'description']

    start_date = forms.DateField(label=_('Write start date'), )
    start_time = forms.TimeField(label=_('Write start time'), )
    due_date = forms.DateField(label=_('Write due date'), required=False)
    due_time = forms.TimeField(label=_('Write due time'), required=False)
    name = forms.CharField(label=_('Write task title'),
                           validators=[MinLengthValidator(5), MaxLengthValidator(100),
                                       RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                      _('Only english and russian letters are allowed, minimum 5 symbols'))])
    description = forms.CharField(label=_('Write description'), required=False,
                                  validators=[MinLengthValidator(5), MaxLengthValidator(300),
                                              RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                             _('Only english and russian letters are allowed, minimum 5 symbols'))])

    def save(self, commit=True):
        instance = super().save(commit=False)
        start_date = self.cleaned_data['start_date']
        start_time = self.cleaned_data['start_time']
        due_date = self.cleaned_data['due_date']
        due_time = self.cleaned_data['due_time']
        instance.start_datetime = combine_date_and_time(start_date, start_time)
        instance.due_datetime = combine_date_and_time(due_date, due_time)
        if commit:
            instance.save()
        return instance

    def clean(self, start_datetime=None, due_datetime=None, update=False):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        due_date = cleaned_data.get('due_date')
        due_time = cleaned_data.get('due_time')
        if start_date and start_time:
            start_datetime = combine_date_and_time(start_date, start_time)
        if due_date and due_time:
            due_datetime = combine_date_and_time(due_date, due_time)
        cleaned_data = super().clean(start_datetime, due_datetime, False)
        validator1 = ValidateDate(field_names=["start_date", "start_time"], days=60, future=True, form=self)
        validator2 = ValidateDate(field_names=["due_date", "due_time"], days=60, future=True, form=self)
        validator1(start_datetime)
        validator2(due_datetime)
        return cleaned_data


class TaskUpdateForm(BaseTaskForm):
    class Meta:
        model = Task
        fields = ['start_datetime', 'due_datetime', 'name', 'description']

    start_datetime = forms.DateTimeField(label=_('Write start date and time'), input_formats=['%Y-%m-%d %H:%M:%S%z'],
                                         validators=[ValidateDate(field_names=["start_datetime"], days=60)])
    due_datetime = forms.DateTimeField(label=_('Write due date and time'), required=False,
                                       input_formats=['%Y-%m-%d %H:%M:%S%z'],
                                       validators=[ValidateDate(field_names=["due_datetime"], days=60)])
    name = forms.CharField(label=_('Write task title'),
                           validators=[MinLengthValidator(5), MaxLengthValidator(100),
                                       RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                      _('Only english and russian letters are allowed, minimum 5 symbols'))])
    description = forms.CharField(label=_('Write description'), required=False,
                                  validators=[MinLengthValidator(5), MaxLengthValidator(300),
                                              RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                             _('Only english and russian letters are allowed, minimum 5 symbols'))])

    def clean(self, start_datetime=None, due_datetime=None, update=False):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        due_datetime = cleaned_data.get('due_datetime')
        cleaned_data = super().clean(start_datetime, due_datetime, True)
        return cleaned_data


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['task_id', 'text']

    task_id = forms.IntegerField(required=False)
    text = forms.CharField(label='comment', validators=[MinLengthValidator(5), MaxLengthValidator(300),
                                                        RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                                       _('Only english and russian letters are allowed, minimum 5 symbols'))])
