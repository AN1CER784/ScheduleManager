from datetime import datetime

from django.core.management.base import BaseCommand

from analysis.models import AnalysisSummary, AnalysisPrompt
from analysis.services.summary_generator import SummaryGenerator
from analysis.utils import get_or_create_report
from tasks.models import Task
from users.models import User


class Command(BaseCommand):
    help = "Creates a summary for user"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('start_date', type=str)
        parser.add_argument('end_date', type=str)
        parser.add_argument('tasks_ids', type=list[int])
        parser.add_argument('--period', type=int, default=1)

    def handle(self, *args, **options):
        user, start_date, end_date, tasks, period = self.get_arguments(**options)
        prompt = AnalysisPrompt.objects.get(period=period)
        analysis_generator = SummaryGenerator(tasks=tasks, prompt=prompt.prompt)
        generated_summary = analysis_generator.generate_summary()
        # generated_summary = "Summary for {} tasks".format(len(tasks))
        report = get_or_create_report(user=user, period=period, start_date=start_date, end_date=end_date)
        print(1, report.report)
        AnalysisSummary.objects.create(report=report, summary=generated_summary)

        self.stdout.write(
            self.style.SUCCESS("Summary {} for {} created successfully".format(report.period,
                                                                               user.username))
        )

    def get_arguments(self, **options):
        user = User.objects.filter(username=options['username']).first()
        start_date, end_date = options['start_date'], options['end_date']
        if isinstance(start_date, str) & isinstance(end_date, str):
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return self.stdout.write(
                    self.style.ERROR("Invalid date format. Use YYYY-MM-DD")
                )
        tasks = Task.objects.filter(id__in=options['tasks_ids'])
        period = options['period']
        if not user or start_date is None or end_date is None or tasks is None:
            return self.stdout.write(
                self.style.ERROR("Clarify username, start_date, end_date, tasks_ids and period.")
            )
        return user, start_date, end_date, tasks, period
