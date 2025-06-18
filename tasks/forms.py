from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils import timezone

from common.validators import ValidateText
from tasks.models import Task, TaskComment
from tasks.utils import combine_date_and_time


class BaseTaskForm(forms.ModelForm):
    def clean(self, start_datetime=None, due_datetime=None, update=False):
        cleaned_data = super().clean()
        if start_datetime:
            self._validate_datetime(start_datetime, 'start', update)
            if due_datetime:
                self._validate_datetime(due_datetime, 'due', update)
                if due_datetime < start_datetime:
                    if not update:
                        fields = ['due_date', 'due_time', ]
                    else:
                        fields = ['due_datetime']
                    for field in fields:
                        self.add_error(field, 'Due date and time must be after start date and time')
        return cleaned_data

    def _validate_datetime(self, datetime, prefix, update):
        if not update:
            fields = [f'{prefix}_date', f'{prefix}_time', ]
            if datetime < timezone.now():
                msg = f'{prefix.capitalize()} date and time must be in the future'
                for field in fields:
                    self.add_error(field, msg)
        else:
            fields = [f'{prefix}_datetime']

        if datetime > timezone.now() + timezone.timedelta(days=60):
            msg = f'{prefix.capitalize()} date and time must be within 2 month'
            for field in fields:
                self.add_error(field, msg)


class TaskCreateForm(BaseTaskForm):
    class Meta:
        model = Task
        fields = ['start_date', 'start_time', 'due_date', 'due_time', 'name', 'description']

    start_date = forms.DateField(label='Write start date')
    start_time = forms.TimeField(label='Write start time')
    due_date = forms.DateField(label='Write due date', required=False)
    due_time = forms.TimeField(label='Write due time', required=False)
    name = forms.CharField(label='Write task title',
                           validators=[MinLengthValidator(5), MaxLengthValidator(100),
                                       ValidateText(field_name="name")])
    description = forms.CharField(label='Write description', required=False,
                                  validators=[MinLengthValidator(5), MaxLengthValidator(300),
                                              ValidateText(field_name="description")])


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
        return cleaned_data


class TaskUpdateForm(BaseTaskForm):
    class Meta:
        model = Task
        fields = ['start_datetime', 'due_datetime', 'name', 'description']


    start_datetime = forms.DateTimeField(label='Write start date and time', input_formats=['%Y-%m-%d %H:%M:%S%z'],)
    due_datetime = forms.DateTimeField(label='Write due date and time', required=False, input_formats=['%Y-%m-%d %H:%M:%S%z'],)
    name = forms.CharField(label='Write task title',
                           validators=[MinLengthValidator(5), MaxLengthValidator(100),
                                       ValidateText(field_name="name")])
    description = forms.CharField(label='Write description', required=False,
                                  validators=[MinLengthValidator(5), MaxLengthValidator(300),
                                              ValidateText(field_name="description")])

    def clean(self, start_datetime=None, due_datetime=None, update=False):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        due_datetime = cleaned_data.get('due_datetime')
        cleaned_data = super().clean(start_datetime, due_datetime, True)
        return cleaned_data



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
