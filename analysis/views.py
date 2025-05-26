from django.views.generic import TemplateView

from analysis.models import AnalysisSummary


class AnalysisView(TemplateView):
    template_name = 'analysis/analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Analysis'
        if self.request.user.is_authenticated:
            context['week_summaries'] = AnalysisSummary.objects.get_summaries_by_period(period=7,
                                                                                        user=self.request.user)
            context['day_summaries'] = AnalysisSummary.objects.get_summaries_by_period(period=1, user=self.request.user)
        return context


