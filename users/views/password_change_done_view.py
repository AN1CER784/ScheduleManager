from django.contrib.auth.views import PasswordChangeDoneView
from django.utils.translation import gettext_lazy as _


class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = "users/password_change_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Password change done')
        return context
