from django.contrib.auth.models import AbstractUser
from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)