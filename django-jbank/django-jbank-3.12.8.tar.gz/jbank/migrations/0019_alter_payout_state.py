# Generated by Django 4.0.6 on 2022-12-09 16:23

from django.db import migrations
import jutil.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("jbank", "0018_alter_referencepaymentbatch_currency_identifier_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payout",
            name="state",
            field=jutil.modelfields.SafeCharField(
                blank=True,
                choices=[
                    ("H", "on hold"),
                    ("W", "waiting processing"),
                    ("U", "waiting upload"),
                    ("D", "uploaded"),
                    ("P", "paid"),
                    ("C", "canceled"),
                    ("E", "error"),
                ],
                db_index=True,
                default="W",
                max_length=1,
                verbose_name="state",
            ),
        ),
    ]
