from django.core.files.storage import default_storage
from django.http import JsonResponse

from uuid import uuid4
from datetime import datetime

from django.conf import settings

ALLOWED_FILE_SIZE = getattr(settings, "PROSE_ATTACHMENT_ALLOWED_FILE_SIZE", 5)


def validate_file(file):
    file_size = file.size / 1024 / 1024
    return file_size <= ALLOWED_FILE_SIZE


def upload_attachment(request):
    if request.method == "POST":
        attachment = request.FILES["file"]
        if not validate_file(attachment):
            return JsonResponse(
                {"error": f"Files must be {ALLOWED_FILE_SIZE}MB or smaller."},
                status=400,
            )
        attachment_dir = datetime.now().strftime("%Y/%m/%d")
        attachment_id = uuid4()
        attachment_extension = attachment.name.split(".")[-1]
        key = f"{attachment_dir}/{attachment_id}.{attachment_extension}"
        path = f"prose/{key}"
        default_storage.save(path, attachment)
        payload = {
            "url": default_storage.url(path),
        }
        return JsonResponse(payload, status=201)
