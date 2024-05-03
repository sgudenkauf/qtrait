from django import forms
from . import models


class CreateFeature(forms.ModelForm):
    class Meta:
        model = models.Feature
        fields = ["name", "description", "featureID", "parentID"]
