from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Case, When, IntegerField
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from users.forms import ProfileForm


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Profile')
        transactions = (self.request.user.bonus_transactions
                        .select_related('task')
                        .order_by('-created_at'))
        context['bonus_transactions'] = transactions[:50]
        aggregates = transactions.aggregate(
            earned=Sum(Case(When(points__gt=0, then='points'), default=0, output_field=IntegerField())),
            spent=Sum(Case(When(points__lt=0, then='points'), default=0, output_field=IntegerField())),
        )
        context['bonus_earned'] = aggregates.get('earned') or 0
        context['bonus_spent'] = abs(aggregates.get('spent') or 0)
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Data updated successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _('Data update error'))
        return super().form_invalid(form)
