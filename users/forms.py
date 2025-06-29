from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordChangeForm, \
    PasswordResetForm as PasswordResetFormCore
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from users.models import User
from users.tasks import reset_password_task_send_mail


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
    password2 = forms.CharField(min_length=8)


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'description']

    image = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.EmailField(disabled=True)
    description = forms.CharField(
        validators=[MinLengthValidator(5), MaxLengthValidator(300), RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                                                   _('Only english and russian letters are allowed, minimum 5 symbols'))],
        required=False)


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField(label=_("New password"), min_length=8)


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
        reset_password_task_send_mail.delay(subject_template_name, email_template_name, context, from_email, to_email,
                                            html_email_template_name, user_id)
