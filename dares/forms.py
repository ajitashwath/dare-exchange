from django import forms
from .models import Dare

class DareForm(forms.ModelForm):
    class Meta:
        model = Dare
        fields = ['name', 'phone_number', 'college', 'dare_text']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Singh',
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'e.g., +91-',
            }),
            'college': forms.TextInput(attrs={
                'placeholder': 'e.g., Lovely Professional University',
            }),
            'dare_text': forms.Textarea(attrs={
                'placeholder': 'Describe the dare in detail...',
                'rows': 5,
            }),
        }

        labels = {
            'name': 'Your Full Name',
            'phone_number': 'Phone Number (for verification only)',
            'dare_text': 'The Dare',
        }
