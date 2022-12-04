# Generated by Django 3.2.16 on 2022-12-04 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_address'),
        ('shopping', '0004_order_ordergoods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.address', verbose_name='收货地址'),
        ),
    ]
