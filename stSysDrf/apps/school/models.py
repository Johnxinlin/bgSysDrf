from django.contrib.auth.models import User
from django.db import models
from utils.modelsMixin import ModelsSetMixin


# Create your models here.

class Classes(ModelsSetMixin):
    name = models.CharField("班级名", max_length=20, unique=True)
    slogan = models.CharField("口号", null=True, blank=True, max_length=50)
    member = models.ManyToManyField(User)

    class Meta:
        db_table = 'classes'
        verbose_name = '班级'
        verbose_name_plural = '班级'
