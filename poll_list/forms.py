from django import forms
from .models import Poll,Choice

class AddPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = [
            'subject',
        ]
class AddChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = [
            'choice_option',
        ]

class SearchForm(forms.Form):
    search = forms.CharField(required=False)