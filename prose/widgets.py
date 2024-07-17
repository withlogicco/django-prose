from django.forms.widgets import Textarea


class RichTextEditor(Textarea):
    template_name = "prose/forms/widgets/editor.html"

    class Media:
        css = {
            "all": (
                "https://unpkg.com/trix@2.1.3/dist/trix.css",
                "prose/editor.css",
            ),
        }
        js = (
            "https://unpkg.com/trix@2.1.3/dist/trix.umd.min.js",
            "prose/editor.js",
        )
