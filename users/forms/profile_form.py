from django import forms
from django.contrib.auth.forms import UserChangeForm
from users.models import User


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['image', 'username', 'email']

    image = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.EmailField(disabled=True)
    # description removed per product scope
