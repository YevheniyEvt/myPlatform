# Generated by Django 5.1.5 on 2025-04-15 17:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('content', models.TextField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('deadline', models.DateField()),
                ('location', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['deadline'],
            },
        ),
        migrations.CreateModel(
            name='TaskUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.BooleanField(default=False)),
                ('revised', models.DateTimeField(blank=True, null=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('not_accepted', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['completed', 'task__deadline'],
            },
        ),
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_time_action', models.DateTimeField(auto_now_add=True)),
                ('revised', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('reopen', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.taskusers')),
            ],
            options={
                'ordering': ['data_time_action'],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='recipients',
            field=models.ManyToManyField(through='tasks.TaskUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]
