from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

from common.mixins import SessionMixin
from tasks.models import Task
from .calendar_builder_service import TaskCalendarBuilder


class ScheduleCalendarView(SessionMixin, ListView):
    template_name = 'schedule/calendar.html'
    paginate_by = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.month_index = None
        self.months_list = None
        self.user_tasks = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_tasks = (
            self.get_owner_filter(model=Task, via='project')
            .select_related('project')
        )
        builder = TaskCalendarBuilder(self.user_tasks)
        builder.build()
        self.months_list, self.month_index = builder.get_months_list, builder.get_current_index

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Calendar')
        context['tasks'] = self.user_tasks
        context['month_datetime'] = self.months_list[context.get('page_obj').number - 1][4][0]

        return context

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_number = self.request.GET.get(self.page_kwarg, self.month_index)
        page = paginator.get_page(page_number)
        return paginator, page, page.object_list, page.has_other_pages()

    def get_queryset(self):
        months = self.months_list
        return months
