# Generated by Django 5.1.5 on 2025-02-19 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunication', '0002_articke_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='articke',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
