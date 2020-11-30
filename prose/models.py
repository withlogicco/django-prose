from django.db import models
from django.utils.html import strip_tags

from prose.fields import DocumentContentField


class AbstractDocument(models.Model):
    content = DocumentContentField()

    def get_plain_text_content(self):
        return strip_tags(self.content)

    def __str__(self):
        plain_text = self.get_plain_text_content()

        if len(plain_text) < 32:
            return plain_text

        return f"{plain_text[:28]}..."

    class Meta:
        abstract = True


class Document(AbstractDocument):
    pass
