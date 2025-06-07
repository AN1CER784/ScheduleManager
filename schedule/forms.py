from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils import timezone

from common.validators import ValidateText
from schedule.models import Task, TaskComment
from schedule.utils import combine_date_and_time


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['start_date', 'start_time', 'due_date', 'due_time', 'name', 'description']

    start_date = forms.DateField(label='Write start date')
    start_time = forms.TimeField(label='Write start time')
    due_date = forms.DateField(label='Write due date')
    due_time = forms.TimeField(label='Write due time')
    name = forms.CharField(label='Write task title',
                           validators=[MinLengthValidator(5), MaxLengthValidator(100),
                                       ValidateText(field_name="name")])
    description = forms.CharField(label='Write description', required=False,
                                  validators=[MinLengthValidator(5), MaxLengthValidator(300),
                                              ValidateText(field_name="description")])

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        due_date = cleaned_data.get('due_date')
        due_time = cleaned_data.get('due_time')
        start_datetime = combine_date_and_time(start_date, start_time)
        due_datetime = combine_date_and_time(due_date, due_time)
        if due_datetime and start_datetime:
            self._validate_datetime(start_datetime, 'start')
            self._validate_datetime(due_datetime, 'due')
            if due_datetime < start_datetime:
                self.add_error('due_date', 'Due date and time must be after start date and time')
                self.add_error('due_time', 'Due date and time must be after start date and time')
        return cleaned_data

    def _validate_datetime(self, datetime, prefix):
        if datetime < timezone.now():
            msg = f'{prefix.capitalize()} date and time must be in the future'
            self.add_error(f'{prefix}_date', msg)
            self.add_error(f'{prefix}_time', msg)
        elif datetime > timezone.now() + timezone.timedelta(days=60):
            msg = f'{prefix.capitalize()} date and time must be within 2 month'
            self.add_error(f'{prefix}_date', msg)
            self.add_error(f'{prefix}_time', msg)

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


class TaskCompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.progress.percentage = 100
        if commit:
            instance.progress.save()
        return instance


class TaskIncompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.progress.percentage = 5
        if commit:
            instance.progress.save()
        return instance


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['task_id', 'text']

    task_id = forms.IntegerField(required=False)
    text = forms.CharField(label='comment', validators=[MinLengthValidator(5), MaxLengthValidator(300), ValidateText(field_name="comment")])
