# Generated by Django 3.1.3 on 2021-01-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_jobactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobactivity',
            name='code_group',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Activity Code Group'),
        ),
        migrations.AlterField(
            model_name='jobactivity',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Activity End Date'),
        ),
        migrations.AlterField(
            model_name='jobactivity',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Activity Start Date'),
        ),
    ]