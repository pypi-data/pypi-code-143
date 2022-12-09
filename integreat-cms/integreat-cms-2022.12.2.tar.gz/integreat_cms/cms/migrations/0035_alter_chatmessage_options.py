# Generated by Django 3.2.15 on 2022-08-26 12:09

from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations

from ..constants import roles

# pylint: disable=unused-argument
def update_roles(apps, schema_editor):
    """
    Update permissions for service and management group

    :param apps: The configuration of installed applications
    :type apps: ~django.apps.registry.Apps

    :param schema_editor: The database abstraction layer that creates actual SQL code
    :type schema_editor: ~django.db.backends.base.schema.BaseDatabaseSchemaEditor
    """
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Emit post-migrate signal to make sure the Permission objects are created before they can be assigned
    emit_post_migrate_signal(2, False, "default")

    # Clear and update permissions according to new constants
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
    Update chat permission field to include default change permission.
    """

    dependencies = [
        ("cms", "0034_organization_region"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chatmessage",
            options={
                "default_permissions": ("delete", "change"),
                "ordering": ["-sent_datetime"],
                "verbose_name": "chat message",
                "verbose_name_plural": "chat messages",
            },
        ),
        migrations.RunPython(update_roles, migrations.RunPython.noop),
    ]
