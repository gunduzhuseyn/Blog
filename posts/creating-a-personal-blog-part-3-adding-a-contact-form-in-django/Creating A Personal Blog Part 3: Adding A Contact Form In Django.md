# Creating And Showing Posts

Hi, and welcome back. In the last part, 
[part 2](https://gunduzhuseyn.com/posts/creating-a-personal-blog-part-2-integrating-a-theme-into-django) of our series, 
I showed you how to download a css theme and integrate it
to our little django project, to make our blog look prettier. However as I said in the previous post, we need great content
as well as the great looks. So we need to be able to create, edit, and publish our posts. 

To do so, we need to create database models to represent our posts, and integrate those models with fronted so we can
filter and show them as needed. If you are not familiar with these concepts, don't worry. To make you get used to the
ropes, I will start small, and simple. In fact, this post will only explain how to enable our users to submit contact
messages to us. By adding this feature, we are dealing with a lot of similar issues that will show up in the future.

## Adding Contact Functionality

So, let's start by providing a contact page for our users, so that they can contact us. If you followed the
previous post, and used the same theme, you should notice that we already have a contact page. In fact if you 
navigate to `http://127.0.0.1:8000/contact/` you will see a nice form where you can submit your messages. 
Currently theme uses javascript to forward the
messages submitted by the users, and if you are proficient in js, it is totally up to you to handle it in this way.
Personally, I would like to use Django, and save the messages in my database.

To save the messages, lets create our first database model, inside _blog/models.py_ file.

```
#!python
from django.db import models


class ContactModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name) + "\t" + str(self.email) + "\t" + str(self.time)

```

In the above code, we are declaring our Contact Model which will exist inside our database as a db table. 
We are also declaring our fields that we want to be populated. name, email, and message will 
be provided by the user, and we will add time of the submission automatically for monitoring purposes. By overwriting str function, we
are determining how our object's name will appear in the Admin panel (more on this soon). Feel free
to add more fields if you want to collect more information from the user, directly or indirectly.

This is the first time we create a model, and every time we create or edit a model, we need to run a few commands, so
Django can create these tables in the database. Remember a warning from previous migrations, complaining about 
unapplied migrations? It is about this issue as well. So to remedy that warning, and apply our newly created model,
go ahead and run these two commands:

```
python manage.py makemigrations
python manage.py migrate
```

Please remember from [part 1](https://gunduzhuseyn.com/posts/creating-a-personal-blog-part-1-setting-up-the-environment) 
of this series, that you need to run python commands from inside a virtual environment, created at the beginning of 
this project. If you are not sure, or do not remember, feel free to go back and take a look. 

Another great thing about Django is that it provides an admin panel, where you can create, edit, and see your objects
directly. To see a model, and its objects, we need to register it in the admin panel, with a few lines of code. 
Go to _admin.py_ file inside _blog_ model, and add these lines:

```
#!python
from django.contrib import admin

from .models import ContactModel


admin.site.register(ContactModel)
```

Now we can create, edit, and see our ContactModel objects. One last step is to create an admin user, so we can login 
to the admin panel. Go ahead and execute the following command from the terminal, and provide required
credentials (email is optional).

```bash
python manage.py createsuperuser
```

We should be good to go now. Start your server and then go to `http://127.0.0.1:8000/admin`, and you should be directed to a log in screen if you
have not logged in as an admin before. Provide your credentials, and login. Then you should be directed to the admin 
panel.

![Admin Panel](imgs/admin_panel.png)

This is where you can create users, and groups, and see your models registered for admin panels. As mentioned above,
you can create Contact objects, by going to the contact models section. However sending messages
over this blog should not only be restricted to yourself. Thus, we need to allow our users to send messages as well,
without needing to access the admin panel.

To enable this, first we need to create a form that will replace the hard coded form inside _contact.html_. 
For this, create a python 
file called _forms.py_ under _blog_ folder, and add the following code to it. 

```
#!python
from django.forms import ModelForm, TextInput, Textarea, EmailInput
from .models import ContactModel


class ContactForm(ModelForm):
    class Meta:
        model = ContactModel
        exclude = ['time']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'email': EmailInput(attrs={'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'placeholder': 'Message'})
        }

```

So, here we create a Django [form](https://docs.djangoproject.com/en/3.0/topics/forms/), that automatically inherits the
fields from the Model we just created. We need to exclude the time field, since it will not be filled by the user. In the
widgets part of the code, we simply add placeholders that will show up if the field is empty. You can customize your
form even more if you want to, but I will keep to the essentials here. If you want to do so, feel free to follow the 
[official guide](https://docs.djangoproject.com/en/3.0/topics/forms/).
Now we need to use this 
form in a view which will serve the contact html page. Django has a class called `FormView` that handles verifying data, 
generating errors, and etc. At this point we are serving our contact page with a simple `TemplateView`, since we did 
not need any major functionality in the view. However, now to make use of the already implemented functionality, we will use
a `FormView`. So go ahead create a view class by inheriting this class, in in _blog/views.py_ file as shown below. By the way
feel free to remove the HomeView class (as well as the url associated with it in _blog/urls.py_ file, and the html file), 
since we will no longer be needing it.

```
#!python
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = 'success'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

```

Above we tell Django which html file to serve, alongside with the form that will show up inside that html file. 
`success_url` parameter determines the url the user will be directed. In our case, Django adds 'success' to the end of 
the current url, and redirects the user there. And once the form is submitted and is valid, meaning there are no
errors, then we save the input received from the user as a Contact object in our database.

There are a few things left to do at this point. First, we need to integrate our form into _contact.html_. And then we should create 
an html page, and a view to handle this page to show the success message, and tie up both these views to urls. 

So lets modify the code inside _contact.html_. We can remove the old hard coded form, and replace it with a more
dynamic django form. This way, if you ever change the form, by adding new fields (spoiler again, we will), then you will not 
need to change a single line from the html page. Go ahead and replace the old form with the new one, by changing the 
code accordingly:

```
#!html
<!-- Main Content -->
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
            <p>Want to get in touch? Fill out the form below to send me a message and I will get back to you as soon as possible!</p>
            <form method="post">
                {% csrf_token %}
                {% for field in form %}
                    <div class="control-group">
                        <div class="form-group floating-label-form-group controls">
                            <label>{{ field.label }}</label>
                            {{ field }}
                            {% for error in field.errors %}
                                <p class="help-block text-danger">{{ error|escape }}</p>
                            {% endfor %}
                        </div>
                    </div>
                {% endfor %}
                <br>
                <div class="form-group">
                    <button type="submit" class="btn btn-primary" id="sendMessageButton">Send</button>
                </div>
            </form>
        </div>
    </div>
</div>
```

Just as a reminder, if things overwhelm you, and you get stuck or confused at any time, feel free to google on these 
materials to get more comfortable. We simply use a for loop in the above code to retrieve each field of the form, 
which will be passed by the view to this html. All the syntax and logic can be looked up on the official [Django 
documentation](https://docs.djangoproject.com/en/3.0/topics/forms/) as well.

Now, lets create an html page called _contact_success.html_ inside the _templates/blog_ folder. 
You can copy and paste the code from _contact.html_, remove the form part, and change the message inside `<p>` tags.

```
#!html
{% extends 'blog/base.html' %}

{% block content %}

{% include 'blog/page_header.html' with header_img_url='/static/img/contact-bg.jpg' header_title='Contact Me' header_subtitle='Have questions? I have answers.' %}

<!-- Main Content -->
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
            <p>Your message has been saved!</p>
        </div>
    </div>
</div>

<hr>

{% endblock %}
```

Since _contact_success.html_ page can be handled by a simple TemplateView class from the _urls.py_ inside blog module,
lets edit the code there, to finally tie up two url patterns to these two views.

```
#!python
from django.urls import path
from django.views.generic import TemplateView

from .views import ContactFormView

urlpatterns = [
    path('index/', TemplateView.as_view(template_name='blog/index.html'), name='index_url'),
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='about_url'),
    path('contact/', ContactFormView.as_view(), name='contact_url'),
    path('contact/success/', TemplateView.as_view(template_name='blog/contact_success.html'), name='about_url'),
    path('post/', TemplateView.as_view(template_name='blog/post.html'), name='post_url'),
]

```

Finally, you should have a working contact page now. I know it may seem as a lot of work at first, especially if you 
are not familiar with Django, but this process will seem much smoother as you get more comfortable. To celebrate, 
navigate to `http://127.0.0.1:8000/contact` and leave yourself a nice message.

![Contact Message](imgs/contact_message.png)

Then go ahead and review your message from the admin panel.

![Admin Panel Contacts](imgs/admin_panel_contacts.png)

Once again, we have achieved our initial goal. And once again, I will ask you to bear with me a little further. We can 
add additional features to our contact system, such as sending an email when someone submits a contact message,
and even replying to those messages from our blog. However, I will leave these to you, as I am confident you will be 
able to add these with ease once you are done with this series. However, I still want to add a feature, that in general
might prepare you a little more for the next posts.

Currently, anyone can submit a contact message, and that is partially good, since we want anyone to be able to reach
us. However, alongside real people, even robots wandering through the internet, filling forms with spam content
might also be interested in filling in this form. A simple way to prevent this is to introduce captcha.
Although they do not prevent all spam, it is still a good practice to add them to public forms. 

## Adding Captcha To Django Forms

If you are looking for a specific functionality in Django (and in other frameworks/languages in general), 
most of the time there is already someone else who tackled the same
issue and shared their code as a Django app. As a result, you can google what you need, find some apps, and decide to
use them or not. When deciding, you should consider whether the app is popular, and up to date, and how much 
customization it allows you. Overall, if it suits your needs go ahead and download it. 
The reason I am telling this is that there is already
an app called [Django Simple Captcha ](https://django-simple-captcha.readthedocs.io/en/latest/usage.html) 
for adding captcha to forms in Django projects.
If in need, please refer to the original app 
[documentation](https://django-simple-captcha.readthedocs.io/en/latest/usage.html). I will explain the steps to install
and use this app.

First we need to install the app, and we can do so using pip. Make sure that you are inside the project's virtual
environment, then execute this command:

```
pip install django-simple-captcha
```

A side note: We are going to be installing a lot of other python modules, so it is a recommended practice to create 
a _requirements.txt_ file in the base of the project, listing all the packages installed, to keep track and also
to install them on other machines with ease.

Our _requirements.txt_ file should look like this at this point.

```
django==2.1.7
django-simple-captcha==0.5.11
```

For any new app we use or create, remember to add it in our _settings.py_ file as always.

```
#!python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'blog',
]
```

Then there are two small initialization steps for this app. 

First include the urls that may be needed for this module in you base _urls.py_ file, under the _myblog_
folder.

```
#!python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('captcha/', include('captcha.urls')),
]
```

Lastly, run migrate command to create any tables that might be needed by the captcha app.

```
python manage.py migrate
```

We should be set for now. Adding a captcha to our form is very simple, thanks to modularity of Django.
We do not need to change our Contact model, as we do not need to store the captcha in our database. 
Thus we can simply add a field to our ContactForm in _forms.py_, and rest will be handled by the app
we just installed.

```
#!python
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

```

We are done. With this last part, I just wanted to show you why we went through all these hassle before. 
As you hopefully see by now, once you build your page in a modular way, then modifying it becomes real
easy.