# Generated by Django 4.1.2 on 2022-12-09 18:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_csf", "0007_auto_20220711_1230"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicallpcsf",
            name="csf_amount_removed",
            field=models.IntegerField(
                blank=True,
                help_text="Units ml",
                null=True,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="CSF amount removed",
            ),
        ),
        migrations.AlterField(
            model_name="lpcsf",
            name="csf_amount_removed",
            field=models.IntegerField(
                blank=True,
                help_text="Units ml",
                null=True,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="CSF amount removed",
            ),
        ),
    ]
