# Generated by Django 4.2.3 on 2023-09-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0038_alter_creditrating_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='is_for_qualified_investors',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
