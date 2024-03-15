from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .models import Club, Process, Envoy


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
        queryset=Envoy.objects.all().values_list("district_name", flat=True).distinct(),
        empty_label="Wszystkie",
        widget=Select2Widget(attrs={"class": "form-select my-3"}),
        required=False,
    )


class ProcessSearchForm(forms.Form):
    state = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Tylko niezakończone",
    )
    document_type = forms.MultipleChoiceField(
        choices=Process.objects.all()
        .values_list("document_type", "document_type")
        .distinct(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
        label="Typ dokumentu",
    )
