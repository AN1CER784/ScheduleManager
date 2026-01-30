from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from users.forms import UserPasswordChangeForm


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Password change')
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Password changed successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _('Password change error'))
        return super().form_invalid(form)
