from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

from users.forms import UserPasswordChangeForm, PasswordResetForm


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password change'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Password change error')
        return super().form_invalid(form)


class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = "users/password_change_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password change done'
        return context


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/emails/password_reset_email_text.html'
    html_email_template_name = 'users/emails/password_reset_email.html'
    form_class = PasswordResetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password reset'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Password reset email sent successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Password reset error')
        return super().form_invalid(form)


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Check your email'
        return context

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password reset confirm'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Password change error')
        return super().form_invalid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password reset complete'
        return context

