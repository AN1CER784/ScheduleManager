from django import forms
from django.utils import timezone

from schedule.models import Task, TaskComment
from .utils import is_meaningful


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['start_date', 'start_time', 'due_date', 'due_time', 'name', 'description']

    start_date = forms.DateField(label='Write start date')
    start_time = forms.TimeField(label='Write start time')
    due_date = forms.DateField(label='Write due date')
    due_time = forms.TimeField(label='Write due time')
    name = forms.CharField(max_length=100, label='Write task title')
    description = forms.CharField(label='Write description', required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')
        due_date = cleaned_data.get('due_date')
        due_time = cleaned_data.get('due_time')
        if start_date and start_time and due_date and due_time:
            start_datetime = timezone.make_aware(
                timezone.datetime.combine(start_date, start_time),
                timezone.get_current_timezone())
            due_datetime = timezone.make_aware(
                timezone.datetime.combine(due_date, due_time),
                timezone.get_current_timezone())
            if start_datetime < timezone.now():
                self.add_error('start_date', 'Start date and time must be in the future')
                self.add_error('start_time', 'Start date and time must be in the future')
            if start_datetime > timezone.now() + timezone.timedelta(days=60):
                self.add_error('start_date', 'Start date and time must be within 2 month')
                self.add_error('start_time', 'Start date and time must be within 2 month')
            if due_datetime < timezone.now():
                self.add_error('due_date', 'Due date and time must be in the future')
                self.add_error('due_time', 'Due date and time must be in the future')
            if due_datetime > timezone.now() + timezone.timedelta(days=60):
                self.add_error('due_date', 'Due date and time must be within 2 month')
                self.add_error('due_time', 'Due date and time must be within 2 month')
            if due_datetime < start_datetime:
                self.add_error('due_date', 'Due date and time must be after start date and time')
                self.add_error('due_time', 'Due date and time must be after start date and time')
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise forms.ValidationError('Task name must be at least 5 characters long')
        elif len(name) > 100:
            raise forms.ValidationError('Task name must be no more than 100 characters long')
        elif not is_meaningful(name):
            raise forms.ValidationError('Task name must be in English or Russian; Give more understandable naming')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            return description
        if len(description) > 300:
            raise forms.ValidationError('Task description must be no more than 300 characters long')
        elif not is_meaningful(description):
            raise forms.ValidationError(
                'Task description must be in English or Russian; Give more understandable description')
        return description


class TaskCompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.complete_percentage = 100
        instance.complete_datetime = timezone.now()
        if commit:
            instance.save()
        return instance


class TaskIncompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = []

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.complete_percentage = 5
        instance.complete_date = None
        if commit:
            instance.save()
        return instance


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['task_id', 'text']

    task_id = forms.IntegerField()
    text = forms.CharField(label='text')

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) > 300:
            raise forms.ValidationError('Comment must be no more than 300 characters long')
        elif len(text) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long')
        elif not is_meaningful(text):
            raise forms.ValidationError('Comment must be in English or Russian; Give more understandable comment')
        return text
