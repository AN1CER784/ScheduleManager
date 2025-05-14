from django import forms
from django.utils import timezone

from schedule.models import Task
from .utils import is_meaningful


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date', 'time', 'name', 'description']

    date = forms.DateField(label='Select a date')
    time = forms.TimeField(label='Select a time')
    name = forms.CharField(max_length=100, label='Write Your task')
    description = forms.CharField(label='Write description')

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        if date and time:
            datetime = timezone.make_aware(
                timezone.datetime.combine(date, time),
                timezone.get_current_timezone())
            if datetime < timezone.now():
                self.add_error('date', error=forms.ValidationError(message='The date and time must be in the future'), )
                self.add_error('time', error=forms.ValidationError(message='The date and time must be in the future'), )
            if datetime > timezone.now() + timezone.timedelta(days=60):
                self.add_error('date',
                               error=forms.ValidationError(message='The date and time must be within 2 month'), )
                self.add_error('time',
                               error=forms.ValidationError(message='The date and time must be within 2 month'), )
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
        if len(description) > 300:
            raise forms.ValidationError('Task description must be no more than 300 characters long')
        if len(description.replace(' ', '')) < 5:
            raise forms.ValidationError('Task description must be at least 5 characters long')
        elif not is_meaningful(description):
            raise forms.ValidationError(
                'Task description must be in English or Russian; Give more understandable description')
        return description


class TaskCompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'status_comment']

    status = forms.BooleanField(label='Task status')
    status_comment = forms.CharField(label='Comment')

    def clean_status_comment(self):
        status_comment = self.cleaned_data['status_comment']
        if len(status_comment) > 300:
            raise forms.ValidationError('Comment must be no more than 300 characters long')
        elif len(status_comment) < 5 and status_comment:
            raise forms.ValidationError('Comment must be at least 5 characters long')
        elif not is_meaningful(status_comment) and status_comment:
            raise forms.ValidationError('Comment must be in English or Russian; Give more understandable comment')
        return status_comment
