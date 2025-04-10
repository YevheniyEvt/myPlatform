# Generated by Django 5.1.5 on 2025-02-17 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0022_rename_allpositions_employeeposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='districtpositions',
            name='position',
            field=models.CharField(choices=[('DM', 'District Manager'), ('DMT', 'District Manager Tranee'), ('RMT', 'Region Manager Trainee'), ('RM', 'Region Manager'), ('CM', 'Country Manager')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='officepositions',
            name='position',
            field=models.CharField(choices=[('BKS', 'Store bookkeper'), ('BKL', 'Logistic bookkeper'), ('BKE', 'Employee bookkeper'), ('BKM', 'Main bookkeper'), ('LS', 'Logigstic Supporter'), ('IT', 'Sys Admin'), ('AU', 'Auditor'), ('FA', 'Facility')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='regionpositions',
            name='position',
            field=models.CharField(choices=[('DM', 'District Manager'), ('DMT', 'District Manager Tranee'), ('RMT', 'Region Manager Trainee'), ('RM', 'Region Manager'), ('CM', 'Country Manager')], max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='storepositions',
            name='position',
            field=models.CharField(choices=[('SM', 'Store Manager'), ('SMT', 'Store Manager Trainee'), ('DepSm', 'DeputyStoreManager'), ('AR', 'Area Responsible'), ('LR', 'Logistic Responsible'), ('SA', 'Sails Assistens')], max_length=50, unique=True),
        ),
    ]
