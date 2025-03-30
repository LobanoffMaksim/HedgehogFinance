# Generated by Django 4.0.5 on 2022-10-17 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bond', '0014_normalvalues_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='industry',
            name='normal_values',
        ),
        migrations.AddField(
            model_name='emitter',
            name='normal_values',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bond.normalvalues'),
        ),
    ]
