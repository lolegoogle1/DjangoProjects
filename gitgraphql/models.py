from django.db import models
from django.forms import TextInput, Textarea


class Customer(models.Model):
    github_login = models.CharField(max_length=200)

    def __str__(self):
        return self.github_login
