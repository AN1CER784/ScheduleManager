from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from analysis.models import AnalysisReport
from common.mixins import CommonFormMixin


class DeleteSummaryView(CommonFormMixin, View):
    def post(self, request, *args, **kwargs):
        report_id = request.POST.get('report_id')
        report = AnalysisReport.objects.get(id=report_id)
        report.delete()
        return JsonResponse(self.response(message=_('Summary was deleted'), item_html=None, success=True))
