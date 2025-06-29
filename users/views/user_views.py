from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from users.forms import LoginForm, ProfileForm, SignupForm
from users.utils import update_projects_user


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Login')
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(self.request,
                             _('%(username)s, You have successfully logged in') % {'username': user.username})
            update_projects_user(session_key, user)
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        if redirect_page != reverse('users:logout') and redirect_page:
            return redirect_page
        return reverse_lazy('users:profile')


class UserSignupView(CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Signup')
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        form.save()
        user = auth.authenticate(self.request, username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password1'])
        auth.login(self.request, user)
        messages.success(self.request,
                         _('%(username)s, You have successfully registered and logged in') % {'username': user.username}
                         )
        update_projects_user(session_key, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        if redirect_page != reverse('users:logout') and redirect_page:
            return redirect_page
        return reverse_lazy('users:profile')


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profile')
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Data updated successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _('Data update error'))
        return super().form_invalid(form)
