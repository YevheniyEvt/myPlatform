# Generated by Django 5.1.5 on 2025-02-27 19:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_alter_task_options_alter_taskusers_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_time_action', models.DateTimeField(auto_now_add=True)),
                ('revised', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('reopen', models.BooleanField(default=False)),
                ('task', models.ManyToManyField(to='tasks.taskusers')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['data_time_action'],
            },
        ),
    ]
