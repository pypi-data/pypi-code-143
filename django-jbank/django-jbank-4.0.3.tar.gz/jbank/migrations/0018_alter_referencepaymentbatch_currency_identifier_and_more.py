# Generated by Django 4.0.4 on 2022-07-02 10:49

from django.db import migrations
import jutil.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("jbank", "0017_alter_statementrecord_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="referencepaymentbatch",
            name="currency_identifier",
            field=jutil.modelfields.SafeCharField(choices=[("1", "EUR")], max_length=3, verbose_name="currency"),
        ),
        migrations.AlterField(
            model_name="referencepaymentbatch",
            name="institution_identifier",
            field=jutil.modelfields.SafeCharField(blank=True, max_length=2, verbose_name="institution"),
        ),
        migrations.AlterField(
            model_name="referencepaymentbatch",
            name="service_identifier",
            field=jutil.modelfields.SafeCharField(blank=True, max_length=9, verbose_name="service"),
        ),
    ]
