from django import forms


class PredictionForm(forms.Form):
    keywords = forms.CharField(max_length=100)
