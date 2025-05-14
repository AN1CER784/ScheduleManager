from django import forms

from schedule.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['date', 'time', 'name', 'description']

    date = forms.DateField(label='Select a date')
    time = forms.TimeField(label='Select a time')
    name = forms.CharField(max_length=100, label='Write Your task')
    description = forms.CharField(label='Write description')


class TaskCompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'status_comment']

    status = forms.BooleanField(label='Task status')
    status_comment = forms.CharField(label='Comment', required=False)

