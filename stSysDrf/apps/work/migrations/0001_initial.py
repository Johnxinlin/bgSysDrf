# Generated by Django 3.2.16 on 2022-11-29 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='标签名')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '标签名',
                'verbose_name_plural': '标签名',
                'db_table': 'label',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('subject', models.TextField(verbose_name='题干')),
                ('type', models.SmallIntegerField(choices=[(0, '单选题'), (1, '多选题'), (2, '判断题'), (3, '填空题'), (4, '问答题')], verbose_name='题目类型')),
                ('score', models.FloatField(blank=True, default=1.0, null=True, verbose_name='分值')),
                ('desciption', models.TextField(blank=True, null=True, verbose_name='题目描述，选项')),
                ('answer', models.TextField(verbose_name='答案')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.label')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
                'db_table': 'topic',
            },
        ),
    ]