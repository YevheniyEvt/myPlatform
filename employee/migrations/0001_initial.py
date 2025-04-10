# Generated by Django 5.1.5 on 2025-02-04 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfficePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_office', models.CharField(choices=[('BK', 'Bookkeper'), ('Ls', 'Logigstic Support'), ('IT', 'Sys Admin'), ('AU', 'Auditor')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RetailPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_retail', models.CharField(choices=[('DM', 'District Manager'), ('DMT', 'District Manager Tranee'), ('RMT', 'Region Manager Trainee'), ('RM', 'Region Manager'), ('CM', 'Country Manager')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StorePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_store', models.CharField(choices=[('SM', 'Store Manager'), ('SMT', 'Store Manager Trainee'), ('DepSm', 'DeputyStoreManager'), ('AR', 'Area Responsible'), ('LR', 'Logistic Responsible'), ('SA', 'Sails Assistens')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_office', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.officeposition')),
                ('position_retail', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.retailposition')),
                ('position_store', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.storeposition')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.position')),
            ],
        ),
    ]
