# Generated by Django 4.2.3 on 2024-12-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0040_alter_finindicator_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='liquidity',
            field=models.BigIntegerField(blank=True, default=1, null=True),
        ),
    ]
