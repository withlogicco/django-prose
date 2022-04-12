from django import forms
from django.db import models

from prose.widgets import RichTextEditor


class RichTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = RichTextEditor
        return super().formfield(**kwargs)


class DocumentContentField(RichTextField):
    pass
