# Generated by Django 2.2.2 on 2019-06-28 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("edc_action_item", "0021_auto_20190628_2113")]

    operations = [
        migrations.RemoveIndex(model_name="actionitem", name="edc_action__action__fe58cb_idx"),
        migrations.RemoveIndex(model_name="actiontype", name="edc_action__name_f674a7_idx"),
        migrations.AddIndex(
            model_name="actionitem",
            index=models.Index(
                fields=[
                    "id",
                    "action_identifier",
                    "action_type",
                    "status",
                    "report_datetime",
                ],
                name="edc_action__id_6cb4e0_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="actiontype",
            index=models.Index(fields=["id", "name"], name="edc_action__id_4feab7_idx"),
        ),
    ]
