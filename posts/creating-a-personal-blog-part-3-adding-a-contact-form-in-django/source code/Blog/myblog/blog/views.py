from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = 'success'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
