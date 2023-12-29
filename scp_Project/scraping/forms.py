from django import forms
from scraping.models import Language

class FindForm(forms.Form):

    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name="slug",
                                      required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Speciality')
