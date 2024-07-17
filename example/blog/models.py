from django.conf import settings
from django.db import models

from prose.fields import RichTextField
from prose.models import Document


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    excerpt = RichTextField(blank=True, default="")
    body = models.OneToOneField(Document, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author.username}: {self.body}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = RichTextField(blank=True, default="")
