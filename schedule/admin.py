
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    ordering = ('-created_at',)