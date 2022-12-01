from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from utils.modelsMixin import ModelsSetMixin


class Label(models.Model):
    name = models.CharField("标签名", max_length=30, unique=True)  # 应该为唯一
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'label'
        verbose_name = '标签名'
        verbose_name_plural = '标签名'

    def __str__(self):
        return self.name


class Topic(ModelsSetMixin):
    TYPE_CHOICES = (
        (0, '单选题'),
        (1, '多选题'),
        (2, '判断题'),
        (3, '填空题'),
        (4, '问答题'),
    )
    subject = models.TextField('题干')
    type = models.SmallIntegerField('题目类型', choices=TYPE_CHOICES)
    score = models.FloatField('分值', default=1.0, null=True, blank=True)
    description = models.TextField('题目描述，选项', null=True, blank=True)
    answer = models.TextField('答案')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        db_table = 'topic'
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['update_time']
