import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Case, When, IntegerField
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse, translate_url
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from users.forms import ProfileForm

logger = logging.getLogger(__name__)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Отображает и обновляет данные профиля авторизованного пользователя."""

    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        """Добавляет в контекст данные по бонусам для карточек профиля."""
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profile')
        transactions = (self.request.user.bonus_transactions
                        .select_related('task')
                        .order_by('-created_at'))
        context['bonus_transactions'] = transactions[:50]
        aggregates = transactions.aggregate(
            earned=Sum(Case(When(points__gt=0, then='points'), default=0, output_field=IntegerField())),
            spent=Sum(Case(When(points__lt=0, then='points'), default=0, output_field=IntegerField())),
        )
        context['bonus_earned'] = aggregates.get('earned') or 0
        context['bonus_spent'] = abs(aggregates.get('spent') or 0)
        return context

    def get_object(self, queryset=None):
        """Разрешает менять только собственный профиль пользователя."""
        return self.request.user

    def form_valid(self, form):
        """Сохраняет профиль и сразу применяет выбранный язык интерфейса."""
        try:
            self.object = form.save()
            selected_language = form.cleaned_data.get('language', settings.LANGUAGE_CODE)
            translation.activate(selected_language)
            self.request.LANGUAGE_CODE = selected_language
            self.request.session['lang_chosen'] = True

            messages.success(self.request, _('Data updated successfully'))
            success_url = translate_url(reverse('users:profile'), selected_language)
            return redirect(success_url)
        except Exception:
            logger.exception('Ошибка при обновлении профиля пользователя id=%s', self.request.user.id)
            raise

    def form_invalid(self, form):
        """Показывает сообщение об ошибке, если форма профиля невалидна."""
        messages.warning(self.request, _('Data update error'))
        return super().form_invalid(form)
