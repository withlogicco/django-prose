from django.core.files.storage import default_storage
from django.http import JsonResponse


def upload_attachment(request):
    if request.method == "POST":
        attachment = request.FILES["file"]
        key = request.POST["key"]
        path = f"prose/{key}"
        default_storage.save(path, attachment)
        payload = {
            "url": default_storage.url(path),
        }
        return JsonResponse(payload, status=201)
