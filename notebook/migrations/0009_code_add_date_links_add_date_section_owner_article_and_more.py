# Generated by Django 5.1.5 on 2025-03-05 11:57

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0008_remove_links_topic_links_section'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 5, 11, 57, 41, 832282, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='links',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 5, 11, 57, 41, 833282, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='section',
            name='owner',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('content', models.TextField(unique=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notebook.section')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notebook.section')),
            ],
        ),
    ]
