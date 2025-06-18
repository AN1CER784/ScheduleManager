from django import forms
from projects.models import Project


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name',]
    name = forms.CharField(min_length=5, required=True)