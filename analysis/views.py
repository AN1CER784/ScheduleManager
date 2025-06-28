from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from analysis.models import AnalysisReport
from common.mixins import JsonFormMixin, CommonFormMixin
from .forms import GenerationForm
from .utils import get_date_range_from_week


class GenerateSummaryView(JsonFormMixin, CommonFormMixin, View):
    def post(self, request, *args, **kwargs):
        period = int(request.POST.get('period'))
        if period == 7:
            start_date, end_date = get_date_range_from_week(request.POST.get('week'))
        else:
            start_date, end_date = (request.POST.get('date') for _ in range(2))
        form = GenerationForm(
            data={'username': request.user.username, 'start_date': start_date, 'end_date': end_date, 'period': period},
            request=request)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse(
            self.response(message=_('Your summary will be generated soon'), item_html=None, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(
            self.response(message=_('Your summary could not be generated'), item_html=item_html, success=False))


class DeleteSummaryView(CommonFormMixin, View):
    def post(self, request, *args, **kwargs):
        report_id = request.POST.get('report_id')
        report = AnalysisReport.objects.get(id=report_id)
        report.delete()
        return JsonResponse(self.response(message=_('Summary was deleted'), item_html=None, success=True))
