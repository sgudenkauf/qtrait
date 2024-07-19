from django import forms
from .models import Project, Service


class UploadFileForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    service_name = forms.CharField(max_length=200)
    file = forms.FileField()
