from django.forms import ModelForm, TextInput, Textarea, EmailInput

from . models import ContactModel
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = ContactModel
        exclude = ['time']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'email': EmailInput(attrs={'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'placeholder': 'Massage'})
        }
