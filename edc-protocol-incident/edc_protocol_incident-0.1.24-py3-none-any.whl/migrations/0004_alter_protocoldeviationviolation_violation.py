# Generated by Django 4.0.4 on 2022-06-02 01:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_protocol_incident", "0003_auto_20211104_1456"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="violation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="edc_protocol_incident.protocolviolations",
                verbose_name="Type of violation",
            ),
        ),
    ]
