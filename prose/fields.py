from django import forms
from django.db import models
import bleach

from prose.widgets import RichTextEditor


ALLOWED_TAGS = [
    "p",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "div",
    "span",
    "a",
    "blockquote",
    "pre",
    "figure",
    "figcaption",
    "br",
    "code",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "picture",
    "source",
    "img",
    "del",
]
ALLOWED_ATTRIBUTES = [
    "alt",
    "class",
    "src",
    "srcset",
    "href",
    "media",
]


class RichTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = RichTextEditor
        return super().formfield(**kwargs)

    def pre_save(self, model_instance, add):
        raw_html = getattr(model_instance, self.attname)
        if not raw_html:
            return raw_html

        sanitized_html = bleach.clean(
            raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES
        )
        return sanitized_html


class DocumentContentField(RichTextField):
    pass
