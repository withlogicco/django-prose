from django.db import models


class Document(models.Model):
    content = models.TextField()
