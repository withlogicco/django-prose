from django.db import models

from prose.widgets import DocumentEditor


class Document(models.Model):
    content = models.TextField()
