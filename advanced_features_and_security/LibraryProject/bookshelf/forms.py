from django import forms

class ExampleForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    publication_year = forms.IntegerField(default=2020)
    ...
    # Add other fields as required
