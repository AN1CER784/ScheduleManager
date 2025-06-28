from modeltranslation.translator import TranslationOptions, register

from main.models import Page


@register(Page)
class NewsTranslationOptions(TranslationOptions):
    fields = ('content',)
