from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import Club, District  # replace with your actual models


class EnvoySearchForm(forms.Form):
    searchEnvoys = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "wyszukaj posła..."}
        ),
    )
    club = forms.ModelMultipleChoiceField(
        queryset=Club.objects.all(),
        widget=Select2MultipleWidget(attrs={"class": "form-check-input"}),
        required=False,
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label="Wszystkie",
        widget=Select2Widget(attrs={"class": "form-select my-3"}),
        required=False,
    )
