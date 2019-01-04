from django.conf import settings
from django.db import models

from prose.fields import DocumentField


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    content = DocumentField()
