# Generated by Django 5.1.5 on 2025-02-27 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comunication', '0012_deletehistory_coment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deletehistory',
            old_name='coment',
            new_name='comment',
        ),
    ]
