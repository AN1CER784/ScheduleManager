from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordChangeForm, \
    PasswordResetForm as PasswordResetFormCore
from django.core.validators import MaxLengthValidator, MinLengthValidator

from common.validators import ValidateText
from users.models import User
from users.tasks import task_send_mail


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'description']

    image = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.EmailField(disabled=True)
    description = forms.CharField(
        validators=[MinLengthValidator(5), MaxLengthValidator(300), ValidateText(field_name='description')],
        required=False)


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()


class PasswordResetForm(PasswordResetFormCore):
    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        user_id = context['user'].id
        context.pop('user')
        task_send_mail.delay(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name, user_id)

