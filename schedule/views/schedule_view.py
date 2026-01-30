from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from projects.models import Project
from schedule.calendar_builder_service import TaskCalendarBuilder
from tasks.models import Task


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = "schedule/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()
        today = timezone.localdate()

        base_qs = (Task.objects
                   .select_related("project", "assignee", "creator")
                   .filter(project__company=user.company))

        project_id = self.request.GET.get("project")
        if project_id:
            base_qs = base_qs.filter(project_id=project_id)

        assignee_id = self.request.GET.get("assignee")
        if assignee_id:
            base_qs = base_qs.filter(assignee_id=assignee_id)

        statuses = self.request.GET.getlist("status")
        if statuses:
            base_qs = base_qs.filter(status__in=statuses)

        period = self.request.GET.get("period", "week")
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if period == "today":
            agenda_start, agenda_end = today, today
        elif period == "month":
            agenda_start = today.replace(day=1)
            agenda_end = (agenda_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        elif period == "custom" and start_date and end_date:
            try:
                agenda_start = timezone.datetime.fromisoformat(start_date).date()
                agenda_end = timezone.datetime.fromisoformat(end_date).date()
            except ValueError:
                agenda_start, agenda_end = today, today + timedelta(days=7)
        else:
            agenda_start, agenda_end = today, today + timedelta(days=7)

        agenda_tasks = (base_qs
                        .filter(deadline__date__range=[agenda_start, agenda_end])
                        .exclude(status=Task.Status.DONE)
                        .order_by("deadline"))

        context["title"] = _("Schedule")
        context["filters"] = {
            "project": project_id or "",
            "assignee": assignee_id or "",
            "status": statuses,
            "period": period,
            "start_date": start_date or "",
            "end_date": end_date or "",
        }
        context["projects"] = Project.objects.filter(company=user.company)
        context["assignees"] = user.company.users.all()
        context["statuses"] = Task.Status.choices

        context["today_tasks"] = (base_qs
                                  .filter(assignee=user, deadline__date=today)
                                  .exclude(status=Task.Status.DONE)
                                  .order_by("deadline"))
        context["week_tasks"] = (base_qs
                                 .filter(assignee=user, deadline__date__range=[today, today + timedelta(days=7)])
                                 .exclude(status=Task.Status.DONE)
                                 .order_by("deadline"))
        context["review_tasks"] = (base_qs
                                   .filter(status=Task.Status.ON_REVIEW, creator=user)
                                   .order_by("deadline"))

        context["overdue_tasks"] = (base_qs
                                    .filter(deadline__lt=now)
                                    .exclude(status=Task.Status.DONE)
                                    .order_by("deadline"))
        context["upcoming_tasks"] = (base_qs
                                     .filter(deadline__date__range=[today, today + timedelta(days=3)])
                                     .exclude(status=Task.Status.DONE)
                                     .order_by("deadline"))

        active_statuses = [Task.Status.NEW, Task.Status.IN_PROGRESS, Task.Status.ON_REVIEW]
        workload = (base_qs
                    .filter(status__in=active_statuses)
                    .values("assignee__username")
                    .annotate(count=models.Count("id"))
                    .order_by("-count"))
        context["workload"] = workload

        context["agenda_tasks"] = agenda_tasks
        context["agenda_range"] = (agenda_start, agenda_end)

        calendar_tasks = base_qs.filter(deadline__isnull=False)
        builder = TaskCalendarBuilder(calendar_tasks)
        builder.build()
        months_list = builder.get_months_list
        month_index = builder.get_current_index
        context["months_list"] = months_list
        context["month_index"] = month_index
        current_month = months_list[month_index - 1] if months_list else []
        context["current_month"] = current_month
        context["month_datetime"] = current_month[4][0] if current_month else timezone.now().date()
        context["tasks"] = calendar_tasks
        return context
