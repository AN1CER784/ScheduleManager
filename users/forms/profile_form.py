from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from users.models import User


class ProfileForm(UserChangeForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'language']

    image = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.EmailField(disabled=True)
    language = forms.ChoiceField(choices=settings.LANGUAGES, required=True)

    def __init__(self, *args, **kwargs):
        """Нормализует текущее значение языка, чтобы поле всегда было валидным."""
        super().__init__(*args, **kwargs)
        raw_language = getattr(self.instance, 'language', None)
        self.fields['language'].initial = self._normalize_language(raw_language)

    def clean_language(self):
        """Проверяет и нормализует выбранный язык профиля."""
        language = self.cleaned_data.get('language')
        return self._normalize_language(language)

    @staticmethod
    def _normalize_language(language):
        """Возвращает поддерживаемый код языка или язык по умолчанию."""
        supported = {code for code, _ in settings.LANGUAGES}
        if language in supported:
            return language
        if isinstance(language, str) and language.lower().startswith('en'):
            return 'en'
        return settings.LANGUAGE_CODE
