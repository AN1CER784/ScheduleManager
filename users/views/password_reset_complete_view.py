from django.contrib.auth.views import PasswordResetCompleteView
from django.utils.translation import gettext_lazy as _


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Password reset complete')
        return context
