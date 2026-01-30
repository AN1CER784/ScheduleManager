from django.contrib.auth.views import PasswordResetDoneView
from django.utils.translation import gettext_lazy as _


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Check your email')
        return context
