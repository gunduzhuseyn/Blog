from django.views.generic import FormView

from .forms import ContactForm
from django.urls import reverse_lazy


class ContactFormView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success_url')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
