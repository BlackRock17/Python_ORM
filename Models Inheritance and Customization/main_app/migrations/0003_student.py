# Generated by Django 4.2.4 on 2023-11-12 17:10

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0002_userprofile_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="Student",
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
                ("name", models.CharField(max_length=100)),
                ("student_id", main_app.models.StudentIDField()),
            ],
        ),
    ]
