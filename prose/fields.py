from django import forms
from django.db import models

from prose.widgets import DocumentEditor


class DocumentContentField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = DocumentEditor
        return super().formfield(**kwargs)
