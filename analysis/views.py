from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from analysis.models import AnalysisSummary


# Create your views here.
class AnalysisView(LoginRequiredMixin, ListView):
    model = AnalysisSummary
    template_name = 'analysis/analysis.html'
    context_object_name = 'all_analysis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Analysis'
        return context

    def get_queryset(self):
        return AnalysisSummary.objects.filter(user=self.request.user)
