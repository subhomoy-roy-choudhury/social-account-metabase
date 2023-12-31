# Generated by Django 4.2.6 on 2023-10-25 20:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LinkedinPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("markdown", models.TextField()),
                (
                    "linkedin_post_id",
                    models.CharField(blank=True, max_length=255, unique=True),
                ),
                ("is_send", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
