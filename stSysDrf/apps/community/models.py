from django.contrib.auth.models import User
from django.db import models
from utils.modelsMixin import ModelsSetMixin, DateTimeModelsMixin
# Create your models here.
from work.models import Label


class Article(ModelsSetMixin):
    STATUS_CHOICES = (
        (0, '未发布'),
        (1, '发布')
    )
    title = models.CharField("标题", max_length=100)
    digest = models.CharField("摘要", max_length=300)
    content = models.TextField("文章内容")
    page_view = models.IntegerField("浏览量", default=0)
    priority = models.IntegerField(verbose_name="优先级", default=0)
    status = models.IntegerField("状态", default=0, choices=STATUS_CHOICES)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-priority', '-page_view', '-create_time']
        db_table = 'article'
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class Comment(DateTimeModelsMixin):
    content = models.TextField("评论内容")
    level = models.IntegerField(verbose_name="评论等级", default=1)
    parent_comment = models.IntegerField("父级评论", null=True, blank=True)
    reply_comment = models.IntegerField("回复评论", null=True, blank=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-create_time']
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name