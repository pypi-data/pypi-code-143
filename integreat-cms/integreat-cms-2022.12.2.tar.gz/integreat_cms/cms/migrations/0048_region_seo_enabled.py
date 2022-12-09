# Generated by Django 3.2.16 on 2022-11-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Add seo_enabled field to region model
    """

    dependencies = [
        ("cms", "0047_poi_meta_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="region",
            name="seo_enabled",
            field=models.BooleanField(
                default=False,
                help_text="Enable possibility to fill meta description for pages, events and locations",
                verbose_name="activate SEO section",
            ),
        ),
    ]
