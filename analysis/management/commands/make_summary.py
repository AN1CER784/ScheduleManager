import datetime

from django.core.management.base import BaseCommand

from analysis.models import AnalysisSummary
from analysis.utils import generate_analysis, structure_tasks
from schedule.models import Task
from users.models import User


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        for user in User.objects.all():
            tasks = Task.objects.filter(user_id=user.id,
                                                   start_date__range=[
                                                       datetime.datetime.now().date() - datetime.timedelta(days=7),
                                                       datetime.datetime.now().date()])
            if not tasks:
                continue
            request = structure_tasks(tasks)
            analysis = generate_analysis(request)
            AnalysisSummary.objects.create(user=user, summary=analysis)

            self.stdout.write(
                self.style.SUCCESS("Summary for {} created successfully".format(user.username))
            )
