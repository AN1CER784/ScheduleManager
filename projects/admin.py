from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'created_by', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('name', 'company__name')
    date_hierarchy = 'created_at'
