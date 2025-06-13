
from django.contrib import admin
from .models import Task, TaskComment, TaskProgress


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    fields = ('task', 'text', 'created_at')
    readonly_fields = ('task', 'text', 'created_at')
    extra = 0

class TaskProgressInline(admin.TabularInline):
    model = TaskProgress
    fields = ('task', 'percentage', 'updated_datetime')
    readonly_fields = ('task', 'updated_datetime')
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')
    list_filter = ('created_at',)
    search_fields = ('name', 'project__name')
    ordering = ('-created_at',)
    inlines = [TaskCommentInline, TaskProgressInline]