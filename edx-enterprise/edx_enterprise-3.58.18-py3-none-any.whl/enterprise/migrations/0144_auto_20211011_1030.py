# Generated by Django 2.2.18 on 2021-10-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0143_auto_20210908_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminnotification',
            name='text',
            field=models.CharField(help_text='Notification banner text which will appear to enterprise admin on admin portal. You can enter maximum of 512 characters. This text support markdown. See https://commonmark.org/help/ for the supported markdown features.', max_length=512),
        ),
    ]
