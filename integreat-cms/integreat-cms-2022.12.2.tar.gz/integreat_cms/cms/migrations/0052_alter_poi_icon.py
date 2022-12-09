# Generated by Django 3.2.16 on 2022-11-22 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """
    Add help text to POI icon field
    """

    dependencies = [
        ("cms", "0051_rename_farsi_flag"),
    ]

    operations = [
        migrations.AlterField(
            model_name="poi",
            name="icon",
            field=models.ForeignKey(
                blank=True,
                help_text="The best results are achieved with images in 16:9 aspect ratio.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pois",
                to="cms.mediafile",
                verbose_name="icon",
            ),
        ),
    ]
