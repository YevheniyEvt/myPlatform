# Generated by Django 5.1.5 on 2025-03-06 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0019_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
