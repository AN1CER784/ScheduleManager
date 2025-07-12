import logging
from typing import Literal

from celery import shared_task
from django.utils import translation

from analysis.notifications import WeekReportNotificationBuilder, DayTaskNotificationBuilder, DayTaskNotificationFetcher
from common.notifications import UserNotificationManager, BuilderProtocol, FetcherProtocol
from tasks.models import Task
from users.models import User
from .models import AnalysisPrompt, AnalysisSummary
from .services.summary_generator import SummaryGenerator

logger = logging.getLogger(__name__)


@shared_task
def make_summary(user_id: int, report_id: int, tasks_ids: list[int], period: Literal[1, 7]) -> None:
    user = User.objects.get(id=user_id)

    with translation.override(user.language):
        prompt = AnalysisPrompt.objects.get(period=period)
        tasks = Task.objects.filter(id__in=tasks_ids)

        if not tasks.exists():
            return

        analysis_generator = SummaryGenerator(tasks=tasks, prompt=prompt.prompt)
        summary_text = analysis_generator.generate_summary()

        if summary_text is None:
            logger.error(f"Failed to generate summary for report {report_id}")
            AnalysisSummary.objects.filter(report_id=report_id).delete()
            return

        logger.info(f"Summary for report {report_id} generated")
        AnalysisSummary.objects.filter(report_id=report_id).update(
            summary=summary_text
        )


@shared_task
def make_week_report() -> None:
    make_report(WeekReportNotificationBuilder)


@shared_task
def make_day_report() -> None:
    make_report(DayTaskNotificationBuilder, DayTaskNotificationFetcher)


def make_report(builder: BuilderProtocol, fetcher: FetcherProtocol | None = None) -> None:
    for user in User.objects.iterator():
        with translation.override(user.language):
            user_notification_manager = UserNotificationManager(user=user, builder=builder, fetcher=fetcher)
            try:
                user_notification_manager.notify()
            except Exception as e:
                logger.exception(f"Failed to send user report {user.id} - {user.email}: {e}")
