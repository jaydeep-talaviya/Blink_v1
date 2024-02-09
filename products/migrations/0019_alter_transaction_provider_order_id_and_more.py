# Generated by Django 4.0.8 on 2024-02-06 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='provider_order_id',
            field=models.CharField(max_length=40, verbose_name='Transaction Order ID'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='signature_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Transaction Signature ID'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_payment_id',
            field=models.CharField(blank=True, max_length=36, null=True, verbose_name='Transaction Payment ID'),
        ),
    ]
