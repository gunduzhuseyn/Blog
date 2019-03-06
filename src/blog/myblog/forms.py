from django.forms import ModelForm, TextInput, Textarea, EmailInput
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ['time']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'})
        }
