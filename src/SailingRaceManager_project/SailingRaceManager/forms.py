from django import forms
from SailingRaceManager.models import *


class NewSeriesForm(forms.ModelForm):
    name = forms.CharField(max_length=50, help_text="Enter a name for the new series")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Series
        fields = ("name",)


class NewHandicapForm(forms.ModelForm):
    boat = forms.CharField(max_length=50, help_text="Enter a name for the new boat")
    handicap = forms.CharField(max_length=50, help_text="Enter a name for the new boat")

    class Meta:
        model = Series
        fields = ("name",)
