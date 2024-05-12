# Generated by Django 5.0.6 on 2024-05-12 10:35

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appka', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('commodity_id', models.AutoField(primary_key=True, serialize=False)),
                ('commodity', models.CharField(max_length=255)),
                ('commodity_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=2)),
                ('country_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='CNCode',
            fields=[
                ('cncode_id', models.AutoField(primary_key=True, serialize=False)),
                ('cncode', models.CharField(max_length=255)),
                ('cncode_active', models.IntegerField(default=1)),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appka.commodity')),
            ],
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('licence_id', models.AutoField(primary_key=True, serialize=False)),
                ('licence_number', models.CharField(max_length=50)),
                ('licence_validity', models.DateTimeField(default=django.utils.timezone.now)),
                ('licence_quantity', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=255)),
                ('licence_active', models.IntegerField(default=1)),
                ('cncode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appka.cncode')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appka.country')),
            ],
        ),
    ]
