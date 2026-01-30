from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from common.mixins import RequestFormKwargsMixin
from users.forms import SignupForm


class UserSignupView(RequestFormKwargsMixin, CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Signup')
        return context

    def form_valid(self, form):
        form.save()
        user = auth.authenticate(self.request, username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password1'])
        auth.login(self.request, user)
        messages.success(self.request,
                         _('%(username)s, You have successfully registered and logged in') % {'username': user.username}
                         )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        if redirect_page != reverse('users:logout') and redirect_page:
            return redirect_page
        return reverse_lazy('users:profile')
