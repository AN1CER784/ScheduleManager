from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from analysis.services.get_reports import get_reports_for_user
from common.mixins import CacheMixin


class AnalysisView(CacheMixin, TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Analysis')
        if self.request.user.is_authenticated:
            query = get_reports_for_user(self.request.user)
            reports = self.find_cache(query, f'summaries_for_user_{self.request.user.id}', 60)
            if reports:
                week_reports = reports[7]
                day_reports = reports[1]
                context['week_reports'] = week_reports
                context['day_reports'] = day_reports
        return context
