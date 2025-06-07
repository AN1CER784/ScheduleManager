from django.views.generic import TemplateView

from analysis.models import AnalysisSummary
from common.mixins import CacheMixin


class AnalysisView(CacheMixin, TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Analysis'
        if self.request.user.is_authenticated:
            week_summaries = AnalysisSummary.objects.get_summaries_by_period(period=7, user=self.request.user)
            day_summaries = AnalysisSummary.objects.get_summaries_by_period(period=1, user=self.request.user)
            context['week_summaries'] = self.find_cache(week_summaries, 'week_summaries_for_user_{self.request.user.id}', 60 * 60 * 24)
            context['day_summaries'] = self.find_cache(day_summaries, f'day_summaries_for_user_{self.request.user.id}', 60 * 60 * 24)
        return context
