from django import forms
from .models import Book

class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Your email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message'})
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name must not contain numbers.")
        return name