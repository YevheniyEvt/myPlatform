# Generated by Django 5.1.5 on 2025-02-24 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_taskusers_end_date_taskusers_not_accepted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskusers',
            name='completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
