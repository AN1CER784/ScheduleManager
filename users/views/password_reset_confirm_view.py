from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Password reset confirm')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Password changed successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _('Password change error'))
        return super().form_invalid(form)
