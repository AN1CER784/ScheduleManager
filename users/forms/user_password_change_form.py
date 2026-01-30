from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField(label=_("New password"), min_length=8)
