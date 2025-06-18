from django.views.generic import TemplateView

from analysis.models import AnalysisSummary
from common.mixins import CacheMixin


class AnalysisView(CacheMixin, TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Analysis'
        if self.request.user.is_authenticated:
            query = AnalysisSummary.objects.get_summaries_by_period(periods=[1,7], user=self.request.user)
            summaries =  self.find_cache(query, 'summaries_for_user_{self.request.user.id}', 60 * 60 * 24)
            if summaries:
                week_summaries = summaries[7]
                day_summaries = summaries[1]
                context['week_summaries'] = week_summaries
                context['day_summaries'] = day_summaries
        return context
