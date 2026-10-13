import shutil
import tempfile
from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT, MEDIA_URL="/media/")
class UploadAttachmentTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def upload(self):
        file = SimpleUploadedFile(
            "page.html", b"<script>alert(1)</script>", content_type="text/html"
        )
        return self.client.post(reverse("prose_upload_attachment"), {"file": file})

    def test_anonymous_upload_is_refused(self):
        response = self.upload()
        self.assertEqual(response.status_code, 403)
        self.assertEqual([p for p in Path(MEDIA_ROOT).rglob("*") if p.is_file()], [])

    def test_signed_in_user_can_upload(self):
        self.client.force_login(User.objects.create_user("writer"))
        response = self.upload()
        self.assertEqual(response.status_code, 201)
        url = response.json()["url"]
        self.assertTrue(url.startswith("/media/prose/"))
        self.assertTrue((Path(MEDIA_ROOT) / url[len("/media/") :]).is_file())

    def test_upload_takes_only_post(self):
        self.client.force_login(User.objects.create_user("writer"))
        response = self.client.get(reverse("prose_upload_attachment"))
        self.assertEqual(response.status_code, 405)
