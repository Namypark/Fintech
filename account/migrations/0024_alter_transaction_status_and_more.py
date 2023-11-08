# Generated by Django 4.2.5 on 2023-11-08 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0023_transaction_amount_currency_alter_transaction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('failed', 'FAILED'), ('completed', 'COMPLETED'), ('pending', 'PENDING'), ('processing', 'PROCESSING'), ('request_sent', 'REQUEST SENT'), ('request_processing', 'REQUEST PROCESSING'), ('request_completed', 'REQUEST COMPLETED')], default='pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('transfer', 'TRANSFER'), ('received', 'RECEIVED'), ('withdraw', 'WITHDRAW'), ('refund', 'REFUND'), ('request', 'REQUEST'), ('none', 'NONE')], default='none', max_length=30),
        ),
    ]
