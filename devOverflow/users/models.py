from django.db import models

class Users(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    bio = models.TextField()
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.png",
        blank=True
    )
    is_curentUser = models.BooleanField(default=0)