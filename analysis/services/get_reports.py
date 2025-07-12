from analysis.models import AnalysisReport
from users.models import User


def get_reports_for_user(user: User) -> dict[int, list['AnalysisReport']]:
    user_reports = AnalysisReport.objects.get_reports(user=user)
    return user_reports

