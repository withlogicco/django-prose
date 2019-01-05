from django import forms
from django.db import models

from prose.widgets import DocumentEditor


class DocumentContentField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = DocumentEditor
        return super().formfield(**kwargs)


class DocumentField(models.OneToOneField):
    def __init__(self, *args, **kwargs):
        super().__init__('prose.Document', models.CASCADE)

    def formfield(self, **kwargs):
        kwargs['widget'] = DocumentEditor
        return super().formfield(**kwargs)
