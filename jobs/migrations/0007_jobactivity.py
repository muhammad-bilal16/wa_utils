# Generated by Django 3.1.3 on 2021-01-10 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20210108_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Activity Code')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('start_date', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Activity Start Date')),
                ('end_date', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Activity End Date')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='jobs.job')),
            ],
        ),
    ]