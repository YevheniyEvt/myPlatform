# Generated by Django 5.1.5 on 2025-02-27 21:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunication', '0008_alter_deletehistory_article_alter_deletehistory_task'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletehistory',
            name='article',
            field=models.BooleanField(default=False),
        ),

        migrations.AlterField(
            model_name='deletehistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
