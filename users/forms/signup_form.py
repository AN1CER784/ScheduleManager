from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from users.models import User, Company


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField(min_length=8)
    company_name = forms.CharField(label=_("Company name"), min_length=2)

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.language = self.request.LANGUAGE_CODE
        company_name = self.cleaned_data["company_name"].strip()
        company, created = Company.objects.get_or_create(name=company_name)
        user.company = company
        user.role = User.Role.ADMIN if created else User.Role.EMPLOYEE
        if commit:
            user.save()
        return user
