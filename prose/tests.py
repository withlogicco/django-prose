import bleach
import nh3
import unittest

# from django.test import TestCase

ALLOWED_TAGS_BLEACH = [
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
ALLOWED_ATTRIBUTES_BLEACH = [
    "alt",
    "class",
    "id",
    "src",
    "srcset",
    "href",
    "media",
]

ALLOWED_TAGS_NH3 = set(ALLOWED_TAGS_BLEACH)
ALLOWED_ATTRIBUTES_NH3 = {"*": set(ALLOWED_ATTRIBUTES_BLEACH)}
assert len(ALLOWED_TAGS_BLEACH) == len(ALLOWED_TAGS_NH3)
assert len(ALLOWED_ATTRIBUTES_BLEACH) == len(ALLOWED_ATTRIBUTES_NH3["*"])

raw_html = """
        <div class="div_tag" id="some_id">
        <p> p <em>em</em>
        <ul>
            <li>li</li>
        </ul>
        <ol>
        <li>li</li>
        </ol>
        <strong>strong</strong>
        <span style="color:darkolivegreen;font-weight:bold">span</span>
        <a href="https://jiri.one">My blog</a>
        <blockquote cite="https://jiri.one">blockquote</blockquote>
        <pre>   both      spaces and
                line breaks
        </pre>
        <figure>
            <img src="pic_trulli.jpg" alt="Trulli" style="width:100%">
            <figcaption>figcaption</figcaption>
        </figure>
        <picture>
            <source media="(min-width:650px)" srcset="img_pink_flowers.jpg">
            <source media="(min-width:465px)" srcset="img_white_flower.jpg">
            <img src="img_orange_flowers.jpg" alt="Flowers" style="width:auto;">
        </picture>
        <code>code</code><br>
        <h1>h1</h1>
        <h2>h2</h2>
        <h3>h3</h3>
        <h4>h4</h4>
        <h5>h5</h5>
        <h6>h6</h6>
        <del>del</del>
        </p>
        </div>
        """


class TestHtmlSanitizer(unittest.TestCase):
    def test_sanitizer_outputs_are_same(self):
        sanitized_html_bleach = bleach.clean(
            raw_html, tags=ALLOWED_TAGS_BLEACH, attributes=ALLOWED_ATTRIBUTES_BLEACH
        )
        sanitized_html_nh3 = nh3.clean(
            raw_html,
            tags=ALLOWED_TAGS_NH3,
            attributes=ALLOWED_ATTRIBUTES_NH3,
            link_rel=None,
        )
        self.assertEqual(sanitized_html_bleach, sanitized_html_nh3)
