# Generated by Django 4.2.3 on 2025-02-27 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0045_report_unit_of_measurement_alter_report_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='first_significant_page',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='last_significant_page',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
