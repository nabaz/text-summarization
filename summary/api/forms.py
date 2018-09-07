from django import forms

class UrlForm(forms.Form):
    url = forms.CharField(label='Url (Wikipedia)')
    summary_sentence = forms.IntegerField(required=False)
