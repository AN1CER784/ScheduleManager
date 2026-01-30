from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from users.forms import PasswordResetForm


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/emails/password_reset_email_text.html'
    html_email_template_name = 'users/emails/password_reset_email.html'
    form_class = PasswordResetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Password reset')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Password reset email sent successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _('Password reset error'))
        return super().form_invalid(form)
