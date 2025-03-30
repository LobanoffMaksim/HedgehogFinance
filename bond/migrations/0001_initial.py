# Generated by Django 4.0.5 on 2022-07-12 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isin', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('is_subordinated', models.BooleanField(blank=True)),
                ('issue_volume', models.BigIntegerField(blank=True)),
                ('placement_date', models.DateField(blank=True)),
                ('maturity_date', models.DateField(blank=True)),
                ('collateral', models.CharField(blank=True, max_length=100)),
                ('moex_id', models.IntegerField(blank=True)),
                ('is_traded_in_TI', models.BooleanField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('current_yield', models.FloatField(blank=True)),
                ('yield_to_maturity', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CouponType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EmitterFinFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(max_length=20)),
                ('fin_file', models.FileField(upload_to='uploads/emitters/')),
            ],
        ),
        migrations.CreateModel(
            name='GuarantorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.industry')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('size', models.FloatField()),
                ('relative_size', models.FloatField()),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.bond')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.currency')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.paymenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Guarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.bond')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.guarantortype')),
            ],
        ),
        migrations.CreateModel(
            name='Emitter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=52)),
                ('moex_id', models.IntegerField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('ceo', models.CharField(blank=True, max_length=48)),
                ('website1', models.URLField(blank=True)),
                ('website2', models.URLField(blank=True)),
                ('is_system_important', models.BooleanField(blank=True)),
                ('akra', models.CharField(blank=True, max_length=8)),
                ('fitch', models.CharField(blank=True, max_length=8)),
                ('ra_expert', models.CharField(blank=True, max_length=8)),
                ('sp', models.CharField(blank=True, max_length=8)),
                ('moodys', models.CharField(blank=True, max_length=8)),
                ('netdebt_to_ebitda', models.FloatField(blank=True)),
                ('netdebt_to_equity', models.FloatField(blank=True)),
                ('netdebt_to_assets', models.FloatField(blank=True)),
                ('revenue', models.BigIntegerField(blank=True)),
                ('fin_data', models.JSONField(blank=True)),
                ('fin_file', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bond.emitterfinfile')),
                ('sector', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bond.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('size', models.FloatField()),
                ('aci', models.FloatField()),
                ('period', models.SmallIntegerField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bond.coupontype')),
            ],
        ),
        migrations.AddField(
            model_name='bond',
            name='coupon',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bond.coupon'),
        ),
        migrations.AddField(
            model_name='bond',
            name='currency',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bond.currency'),
        ),
        migrations.AddField(
            model_name='bond',
            name='emitter',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bond.emitter'),
        ),
    ]
