# Generated by Django 5.1.5 on 2025-03-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunication', '0015_alter_notes_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
