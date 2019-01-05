from django.db import models

from prose.fields import DocumentContentField


class Document(models.Model):
    content = DocumentContentField()
