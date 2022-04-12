from django.urls import path

from prose import views


urlpatterns = [
    path("attachment/", views.upload_attachment, name="prose_upload_attachment"),
]
