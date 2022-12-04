from django.contrib.auth.models import User
from django.db import models

from utils.modelsMixin import ModelsSetMixin


# Create your models here.

class UserDetail(ModelsSetMixin):
    SEX_CHOICES = (
        (0, '女'),
        (1, '男')
    )
    avatar = models.TextField(null=True, blank=True, verbose_name="头像")
    phone = models.CharField(null=True, blank=True, verbose_name="手机号", max_length=11, unique=True)
    age = models.IntegerField(null=True, blank=True, verbose_name="年龄")
    sex = models.IntegerField("性别", null=True, blank=True, choices=SEX_CHOICES)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_detail'
        verbose_name = '用户详情'
        verbose_name_plural = '用户详情'


class Area(models.Model):
    name = models.CharField("地名", max_length=20)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'area'
        verbose_name = "行政区划"
        verbose_name_plural = verbose_name


class Address(ModelsSetMixin):
    name = models.CharField(max_length=40, verbose_name="地址名")
    receiver = models.CharField(max_length=40, verbose_name="收货人")
    province = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name='省', related_name="province_address")
    city = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name='市', related_name="city_address")
    district = models.ForeignKey(Area, on_delete=models.PROTECT, verbose_name='区', related_name="district_address")
    place = models.CharField(max_length=40, verbose_name="详情地址")
    mobile = models.CharField("手机", max_length=11)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")

    class Meta:
        ordering = ['-update_time']
        db_table = 'address'
