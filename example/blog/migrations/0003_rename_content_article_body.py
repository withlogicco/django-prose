# Generated by Django 4.1.5 on 2023-01-27 13:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_article_excerpt"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="content",
            new_name="body",
        ),
    ]
