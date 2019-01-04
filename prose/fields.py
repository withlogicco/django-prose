from django.db.models import TextField

from prose.widgets import DocumentEditor


class DocumentContentField(TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = DocumentEditor
        return super().formfield(**kwargs)
