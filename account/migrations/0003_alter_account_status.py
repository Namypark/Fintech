# Generated by Django 4.2.5 on 2023-09-27 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_account_balance_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('in_active', 'Inactive')], default='in_active', max_length=100),
        ),
    ]
