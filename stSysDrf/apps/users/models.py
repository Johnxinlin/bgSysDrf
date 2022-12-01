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
