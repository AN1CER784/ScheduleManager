from modeltranslation.translator import TranslationOptions, register

from analysis.models import AnalysisPrompt


@register(AnalysisPrompt)
class NewsTranslationOptions(TranslationOptions):
    fields = ('prompt',)
