# Generated by Django 4.2.11 on 2024-06-25 07:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_alter_stock_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='purchase_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='holding',
            name='purchase_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ticker',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
