from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from users.forms import LoginForm


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Login')
        return context

    def form_valid(self, form):
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(self.request,
                             _('%(username)s, You have successfully logged in') % {'username': user.username})
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        if redirect_page != reverse('users:logout') and redirect_page:
            return redirect_page
        return reverse_lazy('users:profile')
