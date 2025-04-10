# Generated by Django 5.1.5 on 2025-03-04 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0005_alter_topic_add_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='code',
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(unique=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notebook.section')),
            ],
        ),
    ]
