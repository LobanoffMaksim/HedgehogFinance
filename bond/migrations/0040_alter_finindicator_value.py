# Generated by Django 4.2.3 on 2024-03-23 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0039_bond_is_for_qualified_investors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finindicator',
            name='value',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
