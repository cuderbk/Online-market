from django import forms

class YearForm(forms.Form):
    year = forms.IntegerField(label='Year')