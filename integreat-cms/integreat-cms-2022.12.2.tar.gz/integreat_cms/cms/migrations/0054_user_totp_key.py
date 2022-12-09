# Generated by Django 3.2.16 on 2022-11-06 20:59
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add a TOTP_key field to the user model to generate time-based on-time passwords for authentication.
    """

    dependencies = [
        ("cms", "0053_alter_role_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="totp_key",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="Will be used to generate TOTP codes",
                max_length=128,
                null=True,
                verbose_name="TOTP key",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="passwordless_authentication_enabled",
            field=models.BooleanField(
                default=False,
                help_text="Enable this option to activate the passwordless login routine for this account",
                verbose_name="Enable passwordless authentication",
            ),
        ),
    ]
