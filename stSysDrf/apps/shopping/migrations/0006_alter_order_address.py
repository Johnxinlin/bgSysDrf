# Generated by Django 3.2.16 on 2022-12-04 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_alter_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(verbose_name='收货地址'),
        ),
    ]
