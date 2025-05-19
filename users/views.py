from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from schedule.models import Task
from users.forms import LoginForm, ProfileForm, SignupForm


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def form_valid(self, form):
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(self.request, f'{user.username}, You have successfully logged in')
            return HttpResponseRedirect(self.get_success_url())

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
        context['title'] = 'Signup'
        return context

    def form_valid(self, form):
        form.save()
        user = form.instance
        auth.login(self.request, user)
        messages.success(self.request, f'{user.username}, You have successfully registered and logged in')
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
        context['title'] = 'Profile'
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Data updated successfully')
        if form.cleaned_data['password2']:
            self.request.user.set_password(form.cleaned_data['password2'])
            self.request.user.save()
            form.save()
            user = form.instance
            auth.login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Data update error')
        return super().form_invalid(form)


class UserScheduleView(LoginRequiredMixin, ListView):
    template_name = 'schedule/schedule.html'
    success_url = reverse_lazy('users:schedule')
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule'
        context['schedule'] = True
        return context

    def get_queryset(self):
        tasks = Task.objects.filter(user_id=self.request.user.id)
        return tasks
