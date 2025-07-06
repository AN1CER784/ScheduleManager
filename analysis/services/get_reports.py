from analysis.models import AnalysisReport


def get_reports_for_user(user):
    query = AnalysisReport.objects.get_reports_by_period(periods=[1, 7], user=user)
    return query

