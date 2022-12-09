# Generated by Django 3.2.11 on 2022-05-18 00:05
from django.db import migrations, models

from ..constants import roles


# pylint: disable=unused-argument
def update_roles(apps, schema_editor):
    """
    Update the role definitions

    :param apps: The configuration of installed applications
    :type apps: ~django.apps.registry.Apps

    :param schema_editor: The database abstraction layer that creates actual SQL code
    :type schema_editor: ~django.db.backends.base.schema.BaseDatabaseSchemaEditor
    """
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    Role = apps.get_model("cms", "Role")

    # Rename municipality team to service team
    municipality_team = Group.objects.get(name="MUNICIPALITY_TEAM")
    municipality_team.name = "SERVICE_TEAM"
    municipality_team.save()
    municipality_team.role.name = "SERVICE_TEAM"
    municipality_team.role.save()

    # Create author role
    author, _ = Group.objects.get_or_create(name="AUTHOR")
    Role.objects.get_or_create(name="AUTHOR", group=author)

    # Assign the correct permissions
    for role_name in dict(roles.CHOICES):
        group, _ = Group.objects.get_or_create(name=role_name)
        # Clear permissions
        group.permissions.clear()
        # Set permissions
        group.permissions.add(
            *Permission.objects.filter(codename__in=roles.PERMISSIONS[role_name])
        )


class Migration(migrations.Migration):
    """
    Migration file to update the role definitions
    """

    dependencies = [
        ("cms", "0024_region_locations_enabled"),
    ]

    operations = [
        migrations.RunPython(update_roles, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="role",
            name="name",
            field=models.CharField(
                choices=[
                    ("MANAGEMENT", "Management"),
                    ("EDITOR", "Editor"),
                    ("AUTHOR", "Author"),
                    ("EVENT_MANAGER", "Event manager"),
                    ("SERVICE_TEAM", "Service team"),
                    ("CMS_TEAM", "CMS team"),
                    ("APP_TEAM", "App team"),
                    ("MARKETING_TEAM", "Marketing team"),
                ],
                max_length=50,
                verbose_name="name",
            ),
        ),
    ]
