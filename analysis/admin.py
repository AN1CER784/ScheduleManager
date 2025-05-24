from django.contrib import admin

from analysis.models import AnalysisSummary


@admin.register(AnalysisSummary)
class AnalysisSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'summary', 'period')
    list_filter = ('user', 'created_at', 'period')
    search_fields = ('user__username', 'created_at')
    list_editable = ('summary',)
