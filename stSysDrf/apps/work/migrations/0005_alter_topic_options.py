# Generated by Django 3.2.16 on 2022-11-29 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0004_alter_label_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['update_time'], 'verbose_name': '题目', 'verbose_name_plural': '题目'},
        ),
    ]