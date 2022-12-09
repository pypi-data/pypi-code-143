# Generated by Django 2.0.2 on 2018-03-19 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_action_item", "0003_auto_20180116_1528")]

    operations = [
        migrations.RenameField(
            model_name="actionitem",
            old_name="parent_model",
            new_name="parent_reference_model",
        ),
        migrations.RenameField(
            model_name="historicalactionitem",
            old_name="parent_model",
            new_name="parent_reference_model",
        ),
        migrations.AlterField(
            model_name="actiontype",
            name="model",
            field=models.CharField(
                blank=True, help_text="reference model", max_length=100, null=True
            ),
        ),
    ]
