from django.forms import ModelForm, TextInput, Textarea, EmailInput, HiddenInput
from .models import Contact

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Contact
        exclude = ['time']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        }
