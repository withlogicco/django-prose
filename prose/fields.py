import html
import json
import re
from urllib.parse import urlsplit

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

# Trix keeps what it knows about an attachment as JSON in data-trix-attachment and
# data-trix-attributes, and needs it to open a saved document again as it was, captions
# included. Trix renders parts of it as HTML (an attachment's "content", for example), so
# these attributes pass only with the keys Trix writes for uploaded files and captions,
# and with http(s) or relative addresses.
TRIX_ATTACHMENT_KEYS = {
    "contentType": str,
    "filename": str,
    "filesize": int,
    "height": int,
    "href": "url",
    "previewable": bool,
    "url": "url",
    "width": int,
}
TRIX_ATTACHMENT_ATTRIBUTE_KEYS = {"caption": str, "presentation": str}


def is_safe_url(value):
    if not isinstance(value, str):
        return False
    try:
        scheme = urlsplit(value).scheme
    except ValueError:  # e.g. "https://[", which is no address at all
        return False
    if scheme:
        return scheme in ("http", "https")
    return not value.startswith("//")


def reject_duplicate_keys(pairs):
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("duplicate key")
    return dict(pairs)


def as_attribute_values(text):
    """The text as browsers write it into a double-quoted attribute (Trix's own output):
    newer ones also escape < and >; bleach, writing it back, escapes only <."""
    value = text.replace("&", "&amp;").replace('"', "&quot;").replace("\xa0", "&nbsp;")
    lt_escaped = value.replace("<", "&lt;")
    return {value, lt_escaped, lt_escaped.replace(">", "&gt;")}


def is_safe_json(value, allowed_keys):
    try:
        # bleach passes attribute values with their character references
        data = json.loads(html.unescape(value), object_pairs_hook=reject_duplicate_keys)
    except (ValueError, RecursionError):  # RecursionError: JSON nested too deep
        return False
    if not isinstance(data, dict):
        return False
    for key, item in data.items():
        kind = allowed_keys.get(key)
        if kind == "url":
            if not is_safe_url(item):
                return False
        elif kind is int:
            if not isinstance(item, int) or isinstance(item, bool):
                return False
        elif kind is None or not isinstance(item, kind):
            return False
    # bleach keeps the attribute as written, so it passes only as the exact JSON Trix writes:
    # anything else (other escapes, duplicate keys) could mean something else to a browser
    # than what was checked here
    canonical = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return value in as_attribute_values(canonical)


def is_allowed_attribute(tag, name, value):
    if name in ALLOWED_ATTRIBUTES:
        return True
    if tag == "figure" and name == "data-trix-attachment":
        return is_safe_json(value, TRIX_ATTACHMENT_KEYS)
    if tag == "figure" and name == "data-trix-attributes":
        return is_safe_json(value, TRIX_ATTACHMENT_ATTRIBUTE_KEYS)
    if tag == "figure" and name == "data-trix-content-type":
        return re.fullmatch(r"[\w.+-]+(/[\w.+-]+)?", value) is not None
    if tag == "img" and name in ("width", "height"):
        return value.isdigit()
    return False


class RichTextField(models.TextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = RichTextEditor
        return super().formfield(**kwargs)

    def pre_save(self, model_instance, add):
        raw_html = getattr(model_instance, self.attname)
        if not raw_html:
            return raw_html

        sanitized_html = bleach.clean(
            raw_html, tags=ALLOWED_TAGS, attributes=is_allowed_attribute
        )
        return sanitized_html


class DocumentContentField(RichTextField):
    pass
