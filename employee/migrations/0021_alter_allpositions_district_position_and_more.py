# Generated by Django 5.1.5 on 2025-02-17 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0020_alter_emploee_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allpositions',
            name='district_position',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.districtpositions'),
        ),
        migrations.AlterField(
            model_name='allpositions',
            name='office_positions',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.officepositions'),
        ),
        migrations.AlterField(
            model_name='allpositions',
            name='region_positions',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.regionpositions'),
        ),
        migrations.AlterField(
            model_name='allpositions',
            name='store_posions',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.storepositions'),
        ),
    ]
