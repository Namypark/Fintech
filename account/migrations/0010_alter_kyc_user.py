# Generated by Django 4.2.5 on 2023-10-04 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_kyc_identity_image_alter_kyc_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kyc',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
    ]