# Generated by Django 4.2.14 on 2024-07-17 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import prose.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0004_alter_article_excerpt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="excerpt",
            field=prose.fields.RichTextField(blank=True, default=""),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", prose.fields.RichTextField(blank=True, default="")),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.article"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]