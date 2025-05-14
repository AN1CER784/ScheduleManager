
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ('name', 'date', 'time', 'status', 'description')
    list_filter = ('status', 'date')
    search_fields = ('name', 'description')
    list_editable = ('status',)