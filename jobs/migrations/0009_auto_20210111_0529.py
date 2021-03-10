# Generated by Django 3.1.3 on 2021-01-11 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0003_auto_20210105_0218'),
        ('jobs', '0008_auto_20210110_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reporting.service'),
        ),
    ]