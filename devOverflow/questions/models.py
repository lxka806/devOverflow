from django.db import models
from users.models import Users

# Create your models here.
class Questions(models.Model):
    title = models.CharField(max_length=200)
    context = models.TextField()
    creator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)