# Generated by Django 2.2.3 on 2019-11-28 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jbank", "0047_wsedisoapcall_error"),
    ]

    operations = [
        migrations.AddField(
            model_name="wsediconnection",
            name="soap_endpoint",
            field=models.URLField(
                default="https://businessws.danskebank.com/financialservice/edifileservice.asmx",
                verbose_name="SOAP endpoint",
            ),
            preserve_default=False,
        ),
    ]
