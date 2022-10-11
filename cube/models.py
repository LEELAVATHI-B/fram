from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class cubeUser(models.Model):
    user_name = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50, unique=True)
    contact_number = models.TextField(max_length=14)
    address = models.TextField()

    def __str__(self):
        return self.user_name
