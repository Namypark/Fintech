# Generated by Django 4.2.5 on 2023-11-21 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_alter_creditcard_card_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='amount_currency',
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='card_number',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]