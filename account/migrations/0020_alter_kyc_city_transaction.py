# Generated by Django 4.2.5 on 2023-10-27 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('account', '0019_alter_kyc_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kyc',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='country', chained_model_field='country', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=15, max_length=20, prefix='TRN', unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('status', models.CharField(choices=[('failed', 'FAILED'), ('completed', 'COMPLETED'), ('pending', 'PENDING'), ('processing', 'PROCESSING')], default='none', max_length=12)),
                ('transaction_type', models.CharField(choices=[('transfer', 'TRANSFER'), ('received', 'RECEIVED'), ('withdraw', 'WITHDRAW'), ('refund', 'REFUND'), ('request', 'REQUEST'), ('none', 'NONE')], default='pending', max_length=12)),
                ('transaction_description', models.CharField(blank=True, default='payment', max_length=1000, null=True)),
                ('reference_number', shortuuid.django_fields.ShortUUIDField(alphabet=None, length=15, max_length=20, prefix='', unique=True)),
                ('transaction_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('transaction_time', models.DateTimeField(auto_now_add=True)),
                ('transaction_time_updated', models.DateTimeField(blank=True, null=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver_account', to='account.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_account', to='account.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]