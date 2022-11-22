# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: modelsMixin.py
@time: 2022/11/18 21:41
"""
from django.db import models


class DateTimeModelsMixin(models.Model):
    """创建与修改时间拓展模型类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True


class IsDeleteModelsMixin(models.Model):
    """逻辑删除模型拓展类"""
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class ModelsSetMixin(DateTimeModelsMixin, IsDeleteModelsMixin):
    """模型拓展整合类"""
    class Meta:
        abstract = True



