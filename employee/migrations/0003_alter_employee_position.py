# Generated by Django 5.1.5 on 2025-02-04 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='employee.position'),
        ),
    ]
