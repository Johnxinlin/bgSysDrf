from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from users.models import Address
from utils.modelsMixin import ModelsSetMixin, DateTimeModelsMixin


class Classification(ModelsSetMixin):
    name = models.CharField("分类名", max_length=40)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'classification'
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Commodity(ModelsSetMixin):
    STATUS_CHOICES = (
        (0, '未发货'),
        (1, '已发货')
    )
    name = models.CharField("商品名", max_length=40)
    caption = models.CharField("副标题", max_length=40)
    brand = models.CharField("品牌", max_length=40, null=True, blank=True)
    price = models.DecimalField("单价", max_digits=10, decimal_places=2)  # max_digits 最大位数 decimal_places小数位数
    stock = models.IntegerField("库存")
    pack = models.TextField("包装信息", null=True, blank=True)
    service_aftersale = models.TextField("售后服务", null=True, blank=True)
    sales = models.IntegerField(default=0, verbose_name="销量")
    comments = models.IntegerField("评价数", default=0)
    status = models.IntegerField("状态", default=0, choices=STATUS_CHOICES)
    detail = models.TextField("详情", null=True, blank=True)
    classification1 = models.ForeignKey(Classification, on_delete=models.PROTECT, verbose_name='一级分类',
                                        related_name='classification1')
    classification2 = models.ForeignKey(Classification, on_delete=models.PROTECT, verbose_name='二级分类',
                                        related_name='classification2', null=True, blank=True)

    class Meta:
        ordering = ['-sales', '-comments', '-create_time']
        db_table = 'commodity'
        verbose_name = "商品"
        verbose_name_plural = verbose_name


class CommodityImg(models.Model):
    src = models.TextField("图片地址")
    priority = models.IntegerField("优先级", default=0)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, verbose_name="商品")

    class Meta:
        ordering = ['-priority']
        db_table = 'commodity_img'
        verbose_name = "商品图"
        verbose_name_plural = verbose_name


class ShoppingCart(DateTimeModelsMixin):
    number = models.IntegerField(default=1, verbose_name="数量")

    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, verbose_name="商品")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")

    class Meta:
        ordering = ['-create_time']
        db_table = 'shopping_cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


class Order(DateTimeModelsMixin):
    PAY_METHOD_CHOICES = (
        (1, '支付宝'),
        (2, '货到付款')
    )
    STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成'),
        (6, '已取消'),
    )
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    total_count = models.IntegerField("商品数", default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额")
    pay_method = models.SmallIntegerField(default=1, verbose_name="支付方式", choices=PAY_METHOD_CHOICES)
    status = models.IntegerField("订单状态", default=1, choices=STATUS_CHOICES)
    address = models.TextField("收货地址")
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.PROTECT)

    class Meta:
        ordering = ['-create_time']
        db_table = 'order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name


class OrderGoods(DateTimeModelsMixin):
    SCORE_CHOICES = (
        (0, '零星'),
        (1, '一星'),
        (2, '二星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星'),
    )
    number = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    comment = models.TextField("评价", null=True, blank=True)
    score = models.IntegerField("评分", choices=SCORE_CHOICES, null=True, blank=True)

    is_anonymous = models.BooleanField(default=False, verbose_name="匿名评价")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    commodity = models.ForeignKey(Commodity, on_delete=models.PROTECT, verbose_name="商品")

    class Meta:
        db_table = "order_goods"
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name


