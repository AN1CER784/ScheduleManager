from datetime import datetime
from typing import Literal, Optional

from django.utils import timezone

from analysis.models import AnalysisReport
from analysis.services.productivity_matrix import TaskAutomatonReport
from users.models import User


def get_date_range_from_week(year_week_str: str) -> tuple[datetime, datetime]:
    year, week = year_week_str.split('-W')
    year, week = int(year), int(week)
    first_day = datetime.fromisocalendar(year, week, 1)
    last_day = datetime.fromisocalendar(year, week, 7)
    return first_day, last_day


def get_or_create_report(user: User, period: Literal[1, 7], start_date: Optional[datetime.date] = None,
                         end_date: Optional[datetime.date] = None) -> AnalysisReport:
    if start_date is None and end_date is None:
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=period + 1)
    report = AnalysisReport.objects.filter(user=user, period=period, start_date=start_date, end_date=end_date).first()
    if not report:
        report_json = TaskAutomatonReport(user=user, period=period, start_date=start_date,
                                          end_date=end_date).generate_report()
        report = AnalysisReport.objects.create(user=user, report=report_json, period=period, start_date=start_date,
                                               end_date=end_date)
    return report
