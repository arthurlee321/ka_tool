# Generated by Django 5.0 on 2023-12-17 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('overlap_day_before', models.IntegerField()),
                ('overlap_day_after', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('sku_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wsp', models.DecimalField(decimal_places=2, max_digits=6)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('multi_buy', models.IntegerField()),
                ('net_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricesetter.customer')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricesetter.sku')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_start', models.DateField()),
                ('promo_end', models.DateField()),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pricesetter.pricing')),
            ],
        ),
    ]
