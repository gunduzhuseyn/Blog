from django.db import models


class ContactModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name) + "\t" + str(self.email) + "\t" + str(self.time)
