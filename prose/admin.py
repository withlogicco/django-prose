from django.contrib import admin
from django.db import models

from prose.models import Document
from prose.widgets import DocumentEditor


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            'widget': DocumentEditor,
        },
    }
