# Generated by Django 2.2.28 on 2022-08-16 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("swh_web_add_forge_now", "0007_rename_denied_request_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="forge_url",
            field=models.URLField(),
        ),
    ]
