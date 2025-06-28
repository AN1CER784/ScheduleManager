from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from main.models import Page


@admin.register(Page)
class ProjectAdmin(TranslationAdmin):
    list_display = ('key', 'content')
    list_editable = ('content',)
