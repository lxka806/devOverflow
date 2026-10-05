from django.db import models

class Users(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    bio = models.TextField()
    is_curentUser = models.BooleanField(default=0)