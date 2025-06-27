from django.contrib import admin

from analysis.models import AnalysisReport, AnalysisSummary, AnalysisPrompt


class AnalysisSummaryInline(admin.TabularInline):
    model = AnalysisSummary
    fields = ('summary',)

@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'end_date', 'report', 'period')
    list_filter = ('user', 'start_date', 'end_date', 'period')
    search_fields = ('user__username', 'start_date', 'end_date',)
    list_editable = ('period',)
    inlines = [AnalysisSummaryInline]


@admin.register(AnalysisPrompt)
class AnalysisPromptAdmin(admin.ModelAdmin):
    list_display = ('period', 'prompt')
    list_editable = ('prompt',)
    list_filter = ('period',)
    search_fields = ('period',)