from django.core.management.base import BaseCommand
from django.utils import timezone

from analysis.models import AnalysisSummary
from analysis.utils import generate_analysis, structure_tasks
from projects.models import Project
from tasks.models import Task
from users.models import User


class BaseMakeSummaryCommand(BaseCommand):
    def __init__(self, prompt, days):
        super().__init__()
        self.prompt = prompt
        self.days = days

    help = "Creates a summary for each active user"

    def handle(self, *args, **options):
        for user in User.objects.all():
            projects = Project.objects.filter(user=user)
            tasks = Task.objects.filter(project__in=projects).filter(start_datetime__range=[
                timezone.now() - timezone.timedelta(days=self.days),
                timezone.now()])
            if not tasks:
                continue
            request = structure_tasks(tasks)
            analysis = generate_analysis(request, self.prompt)
            summary = AnalysisSummary.objects.create(user=user, summary=analysis,
                                                     period=self.days)

            self.stdout.write(
                self.style.SUCCESS("Summary {} for {} created successfully".format(summary.period,
                                                                                   user.username))
            )
