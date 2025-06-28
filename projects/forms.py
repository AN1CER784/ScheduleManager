from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from projects.models import Project


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', ]

    name = forms.CharField(min_length=5, required=True, validators=[RegexValidator(r'^(?=.*[a-zA-Zа-яА-ЯёЁ]).{5,}$',
                                                                                   _('Only english and russian letters are allowed, minimum 5 symbols'),
                                                                                   'invalid')])
