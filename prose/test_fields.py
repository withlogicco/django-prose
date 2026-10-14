from django.test import TestCase

from prose.models import Document

# a picture with a caption, as Trix 2 writes it after an upload through prose
ATTACHMENT = (
    '<figure data-trix-attachment="{&quot;contentType&quot;:&quot;image/png&quot;,'
    "&quot;filename&quot;:&quot;photo.png&quot;,&quot;filesize&quot;:2074,"
    "&quot;height&quot;:200,&quot;href&quot;:&quot;/media/prose/photo.png"
    "?content-disposition=attachment&quot;,&quot;url&quot;:&quot;/media/prose/photo.png"
    '&quot;,&quot;width&quot;:300}" data-trix-content-type="image/png" '
    'data-trix-attributes="{&quot;caption&quot;:&quot;A caption&quot;,'
    '&quot;presentation&quot;:&quot;gallery&quot;}" '
    'class="attachment attachment--preview attachment--png">'
    '<a href="/media/prose/photo.png?content-disposition=attachment">'
    '<img src="/media/prose/photo.png" width="300" height="200">'
    '<figcaption class="attachment__caption attachment__caption--edited">A caption</figcaption>'
    "</a></figure>"
)


class RichTextFieldTests(TestCase):
    def save(self, content):
        document = Document.objects.create(content=content)
        document.refresh_from_db()
        return document.content

    def test_attachments_keep_what_trix_needs_to_open_them_again(self):
        content = self.save(ATTACHMENT)
        for attribute in (
            'data-trix-attachment="{&quot;contentType&quot;:&quot;image/png&quot;',
            'data-trix-attributes="{&quot;caption&quot;:&quot;A caption&quot;',
            'data-trix-content-type="image/png"',
            'width="300"',
            'height="200"',
        ):
            self.assertIn(attribute, content)

    def test_attachment_json_with_html_or_unsafe_addresses_is_dropped(self):
        for data in (
            # Trix renders an attachment's "content" as HTML
            "{&quot;contentType&quot;:&quot;image/png&quot;,"
            "&quot;content&quot;:&quot;&lt;img src=x onerror=alert(1)&gt;&quot;}",
            "{&quot;contentType&quot;:&quot;image/png&quot;,"
            "&quot;url&quot;:&quot;javascript:alert(1)&quot;}",
        ):
            content = self.save(
                f'<figure data-trix-attachment="{data}" class="attachment"></figure>'
            )
            self.assertNotIn("data-trix-attachment", content)
        content = self.save(
            '<figure data-trix-attributes="{&quot;href&quot;:'
            '&quot;javascript:alert(1)&quot;}"></figure>'
        )
        self.assertNotIn("data-trix-attributes", content)

    def test_attachment_json_that_could_read_differently_is_dropped(self):
        for data in (
            # Python drops the &#127; and sees one "href", a browser keeps two keys
            "{&quot;href&quot;:&quot;javascript:alert(1)&quot;,"
            "&quot;hr&#127;ef&quot;:&quot;https://example.com&quot;}",
            # not the way Trix writes it
            "{&quot;width&quot;: 300}",
            # no address at all
            "{&quot;url&quot;:&quot;https://[&quot;}",
        ):
            content = self.save(f'<figure data-trix-attachment="{data}"></figure>')
            self.assertNotIn("data-trix-attachment", content)

    def test_caption_with_angle_brackets_both_ways_browsers_write_it(self):
        for caption in ("1 < 2", "1 &lt; 2"):  # newer browsers escape < and > too
            data = f"{{&quot;caption&quot;:&quot;{caption}&quot;}}"
            content = self.save(f'<figure data-trix-attributes="{data}"></figure>')
            self.assertIn("data-trix-attributes", content)

    def test_attachment_json_stays_when_a_document_is_saved_again(self):
        for name, data in (
            # older browsers write < and > as they are, newer ones escape both
            ("data-trix-attributes", "{&quot;caption&quot;:&quot;<photo>&quot;}"),
            ("data-trix-attributes", "{&quot;caption&quot;:&quot;&lt;photo&gt;&quot;}"),
            ("data-trix-attachment", "{&quot;filename&quot;:&quot;<a>.png&quot;}"),
        ):
            document = Document.objects.create(
                content=f'<figure {name}="{data}"></figure>'
            )
            document.refresh_from_db()
            document.save()  # bleach wrote < back as &lt; but left > as it was
            document.refresh_from_db()
            self.assertIn(name, document.content)

    def test_json_nested_too_deep_is_dropped(self):
        data = "[" * 100000 + "]" * 100000
        content = self.save(f'<figure data-trix-attachment="{data}"></figure>')
        self.assertNotIn("data-trix-attachment", content)

    def test_scripts_and_event_handlers_are_still_removed(self):
        content = self.save(
            '<img src="photo.png" onerror="alert(1)"><script>alert(2)</script>'
        )
        self.assertNotIn("onerror", content)
        self.assertNotIn("<script>", content)
