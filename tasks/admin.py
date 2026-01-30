
from django.contrib import admin
from .models import Task, TaskComment, TaskResult, TaskChangeLog


class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    fields = ('author', 'text', 'created_at')
    readonly_fields = ('author', 'text', 'created_at')
    extra = 0


class TaskResultInline(admin.TabularInline):
    model = TaskResult
    fields = ('author', 'message', 'created_at')
    readonly_fields = ('author', 'message', 'created_at')
    extra = 0


class TaskChangeLogInline(admin.TabularInline):
    model = TaskChangeLog
    fields = ('changed_by', 'field_name', 'old_value', 'new_value', 'created_at')
    readonly_fields = ('changed_by', 'field_name', 'old_value', 'new_value', 'created_at')
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'assignee', 'deadline')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'project__name', 'assignee__username')
    ordering = ('-created_at',)
    inlines = [TaskCommentInline, TaskResultInline, TaskChangeLogInline]
