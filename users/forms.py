from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from ScheduleManager.utils import is_meaningful
from users.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['image', 'username', 'password1', 'password2', 'description']

    image = forms.ImageField(required=False)
    username = forms.CharField()
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        user = self.instance

        if password1 == '' and password2:
            self.add_error('password1',
                           error=ValidationError(message='You must enter your current password to set a new one.'), )

        elif password2 and not user.check_password(password1):
            self.add_error('password1', error=ValidationError(message='Your current password is incorrect.'), )

        elif password1 and password2 == '':
            self.add_error('password2', error=ValidationError(message='You must enter a new password to set.'), )

        elif password1 and password2:
            try:
                validate_password(password2, user)
            except ValidationError as e:
                self.add_error('password2', error=e)

        return cleaned_data

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            return description
        elif len(description) > 300:
            raise forms.ValidationError('Description must be no more than 300 characters long')
        elif not is_meaningful(description):
            raise forms.ValidationError(
                'Task description must be in English or Russian; Give more understandable description')
        return description



