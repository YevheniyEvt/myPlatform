# Generated by Django 5.1.5 on 2025-02-04 18:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_rename_office_position_officeposition_user_position_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPosition',
            new_name='Position',
        ),
    ]
