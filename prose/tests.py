import shutil
import tempfile
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse


class UploadAttachmentTests(TestCase):
    def setUp(self):
        # a media directory of its own for every test, so the tests can run in any order
        self.media_root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.media_root, ignore_errors=True)
        media = override_settings(MEDIA_ROOT=str(self.media_root), MEDIA_URL="/media/")
        media.enable()
        self.addCleanup(media.disable)

    def upload(self):
        file = SimpleUploadedFile(
            "page.html", b"<script>alert(1)</script>", content_type="text/html"
        )
        return self.client.post(reverse("prose_upload_attachment"), {"file": file})

    def test_anonymous_upload_is_refused(self):
        response = self.upload()
        self.assertEqual(response.status_code, 403)
        self.assertEqual([p for p in self.media_root.rglob("*") if p.is_file()], [])

    def test_signed_in_user_can_upload(self):
        self.client.force_login(User.objects.create_user("writer"))
        response = self.upload()
        self.assertEqual(response.status_code, 201)
        url = response.json()["url"]
        self.assertTrue(url.startswith("/media/prose/"))
        self.assertTrue((self.media_root / url[len("/media/") :]).is_file())

    def test_upload_takes_only_post(self):
        self.client.force_login(User.objects.create_user("writer"))
        response = self.client.get(reverse("prose_upload_attachment"))
        self.assertEqual(response.status_code, 405)
