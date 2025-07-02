from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from common.validators import ValidateDate
from tasks.models import Task
from .models import PERIOD_CHOICES, AnalysisSummary
from .tasks import make_summary
from .utils import get_or_create_report


class GenerationForm(forms.Form):
    start_date = forms.DateTimeField(
        label=_('Select date'),
        validators=[ValidateDate(field_names=["start_date"], days=120, future=False)]
    )
    end_date = forms.DateTimeField()
    period = forms.TypedChoiceField(
        choices=PERIOD_CHOICES,
        coerce=int
    )

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        period = cleaned_data.get('period')

        if not (start_date and end_date and period):
            return cleaned_data

        report = self._get_or_create_report(period, start_date.date(), end_date.date())

        if AnalysisSummary.objects.filter(report=report).exists():
            self.add_error(
                'start_date',
                _("A summary already exists for the selected period and date.")
            )
            return cleaned_data

        tasks = self._get_tasks_in_range(start_date, end_date)

        if not tasks.exists():
            self.add_error(
                'start_date',
                _("No tasks found for the selected period.")
            )
            return cleaned_data

        cleaned_data.update({
            'report': report,
            'tasks': tasks
        })

        return cleaned_data

    def save(self):
        report = self.cleaned_data['report']
        tasks = self.cleaned_data['tasks']
        period = self.cleaned_data['period']
        AnalysisSummary.objects.create(
            report=report,
        )

        make_summary.delay(
            user_id=self.request.user.id,
            report_id=report.id,
            tasks_ids=list(tasks.values_list('id', flat=True)),
            period=period
        )

    def _get_or_create_report(self, period, start_date, end_date):
        return get_or_create_report(
            user=self.request.user,
            period=period,
            start_date=start_date,
            end_date=end_date
        )

    def _get_tasks_in_range(self, start_date, end_date):
        return Task.objects.filter(
            project__user=self.request.user
        ).filter(
            Q(start_datetime__date__range=(start_date, end_date)) |
            Q(due_datetime__date__range=(start_date, end_date))
        ).select_related('project')
