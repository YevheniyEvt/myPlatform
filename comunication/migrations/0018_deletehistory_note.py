# Generated by Django 5.1.5 on 2025-03-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunication', '0017_alter_notes_options_alter_notes_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='deletehistory',
            name='note',
            field=models.BooleanField(default=False),
        ),
    ]
