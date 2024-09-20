from django import forms
from .models import Project, Service


from django import forms


from django import forms
from .models import Project


class XMLUploadForm(forms.Form):
    xml_file = forms.FileField(label="XML Datei")
    existing_project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="Projekt wählen",
    )
    new_project_name = forms.CharField(
        max_length=200, required=False, label="Projektname"
    )
    new_project_owner = forms.CharField(max_length=200, required=False, label="Owner")
    new_project_description = forms.CharField(
        widget=forms.Textarea, required=False, label="Description"
    )

    def clean(self):
        cleaned_data = super().clean()
        existing_project = cleaned_data.get("existing_project")
        new_project_name = cleaned_data.get("new_project_name")

        if not existing_project and not new_project_name:
            raise forms.ValidationError(
                "Bitte ein bestehendes Projekt auswählen oder ein neues Projekt anlegen."
            )

        return cleaned_data
