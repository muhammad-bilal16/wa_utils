# Generated by Django 3.1.3 on 2021-01-03 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='subby_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='Subby Rate'),
        ),
        migrations.AlterField(
            model_name='services',
            name='wa_utilities_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='WA Utilities Rate'),
        ),
    ]