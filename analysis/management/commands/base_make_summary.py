from django.core.management.base import BaseCommand

from analysis.models import AnalysisSummary
from analysis.utils import generate_analysis, structure_tasks
from schedule.models import Task
from users.models import User
from django.utils import timezone


class BaseMakeSummaryCommand(BaseCommand):
    def __init__(self, prompt, days):
        super().__init__()
        self.prompt = prompt
        self.days = days

    help = "Creates a summary for each active user"

    def handle(self, *args, **options):
        for user in User.objects.all():
            tasks = Task.objects.filter(user_id=user.id,
                                        start_date__range=[
                                            timezone.now() - timezone.timedelta(days=self.days),
                                            timezone.now()]) | Task.objects.filter(user_id=user.id,
                                                                                                   complete_datetime__range=[
                                                                                                       timezone.now() - timezone.timedelta(
                                                                                                           days=self.days),
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
