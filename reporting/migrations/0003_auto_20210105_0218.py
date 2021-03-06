# Generated by Django 3.1.3 on 2021-01-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_auto_20210103_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=1000, null=True, unique=True, verbose_name='New Service Code')),
                ('sap_code', models.CharField(blank=True, max_length=1000, null=True, verbose_name='SAP Code')),
                ('drawing', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Drawing')),
                ('service_type', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Service Type')),
                ('service_description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Service Description')),
                ('rate_type', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Rate Type')),
                ('notes', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Notes')),
                ('wa_utilities_rate', models.FloatField(blank=True, null=True, verbose_name='WA Utilities Rate')),
                ('subby_rate', models.FloatField(blank=True, null=True, verbose_name='Subby Rate')),
            ],
        ),
        migrations.DeleteModel(
            name='Services',
        ),
    ]
