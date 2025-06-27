from django.views.generic import TemplateView

from analysis.models import AnalysisReport
from common.mixins import CacheMixin


class AnalysisView(CacheMixin, TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Analysis'
        if self.request.user.is_authenticated:
            query = AnalysisReport.objects.get_reports_by_period(periods=[1, 7], user=self.request.user)
            reports = query
            if reports:
                week_reports = reports[7]
                day_reports = reports[1]
                context['week_reports'] = week_reports
                context['day_reports'] = day_reports
        return context