# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jbank", "0008_auto_20171103_0007"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statementrecord",
            name="remittance_info",
            field=models.CharField(blank=True, db_index=True, max_length=32, verbose_name="remittance info"),
        ),
    ]
