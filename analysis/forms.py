from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from common.validators import ValidateDate
from tasks.models import Task
from .models import AnalysisReport
from .models import PERIOD_CHOICES
from .tasks import make_summary


class GenerationForm(forms.Form):
    class Meta:
        fields = ['start_date', 'end_date', 'period', 'username']

    username = forms.CharField()
    start_date = forms.DateTimeField(label=_('Select date'),
                                     validators=[ValidateDate(field_names=["start_date"], days=120, future=False)])
    end_date = forms.DateTimeField()
    period = forms.TypedChoiceField(choices=PERIOD_CHOICES, coerce=int)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        period = cleaned_data.get('period')
        if start_date and end_date:
            report = AnalysisReport.objects.filter(user=self.request.user, start_date=start_date, end_date=end_date, period=period).first()
            summary = report.summary if report else None
            if summary:
                self.add_error("start_date", _("A summary already exists for the selected period and date."))
            tasks = Task.objects.filter(project__user=self.request.user).select_related('project').filter(
                Q(start_datetime__date__range=[
                    start_date,
                    end_date]) |
                Q(due_datetime__date__range=[
                    start_date,
                    end_date]))
            if not tasks:
                self.add_error("start_date", _("No tasks found for the selected period."))
            cleaned_data['tasks'] = tasks

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self):
        period = self.cleaned_data.get('period')
        username = self.cleaned_data.get('username')
        start_date = self.cleaned_data.get('start_date').date()
        end_date = self.cleaned_data.get('end_date').date()
        tasks = self.cleaned_data.get('tasks')
        tasks_ids = list(tasks.values_list('id', flat=True))
        make_summary.delay(username=username, start_date=start_date, end_date=end_date, tasks_ids=tasks_ids,
                           period=period)
