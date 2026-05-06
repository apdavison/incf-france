from django import forms
from .models import Researcher, Team, Project


class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        exclude = ('id', 'team')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ('id',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('id',)
