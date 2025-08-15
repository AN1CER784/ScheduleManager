from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from analysis.models import AnalysisReport



class AnalysisView(TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Analysis')
        if self.request.user.is_authenticated:
            reports = AnalysisReport.objects.get_reports(user=self.request.user)
            if reports:
                week_reports = reports[7]
                day_reports = reports[1]
                context['week_reports'] = week_reports
                context['day_reports'] = day_reports
        return context
