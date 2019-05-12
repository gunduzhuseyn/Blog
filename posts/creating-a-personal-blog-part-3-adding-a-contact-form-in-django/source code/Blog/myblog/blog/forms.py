from captcha.fields import CaptchaField
from django.forms import ModelForm, TextInput, Textarea, EmailInput
from .models import ContactModel


class ContactForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = ContactModel
        exclude = ['time']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'email': EmailInput(attrs={'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'placeholder': 'Message'})
        }
