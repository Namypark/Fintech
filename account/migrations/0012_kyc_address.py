# Generated by Django 4.2.5 on 2023-10-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_kyc_account_alter_kyc_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]