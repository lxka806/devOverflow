
from django.db import models
from users.models import Users


class Questions(models.Model):
    title = models.CharField(max_length=200)
    context = models.TextField()

    creator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    author = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    context = models.TextField()

    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.name}"
