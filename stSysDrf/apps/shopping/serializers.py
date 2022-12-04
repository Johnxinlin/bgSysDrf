# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: serializers.py
@time: 2022/12/3 16:35
"""
import datetime
import random
from decimal import Decimal

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db import transaction

from shopping.models import Classification, Commodity, CommodityImg, ShoppingCart, Order, OrderGoods
from users.models import Address


class ClassificationSerializer(ModelSerializer):
    class Meta:
        model = Classification
        fields = ['id', 'name']


class ParentClassificationSerializer(ModelSerializer):
    classification_set = ClassificationSerializer(many=True, read_only=True)

    class Meta:
        model = Classification
        fields = ['id', 'name', 'classification_set', 'parent']


class CommodityImgSerializer(ModelSerializer):
    class Meta:
        model = CommodityImg
        fields = ['src']


class CommoditySerializer(ModelSerializer):
    classification1_name = serializers.CharField(source='classification1.name', read_only=True)
    classification2_name = serializers.CharField(source='classification2.name', read_only=True)

    class Meta:
        model = Commodity
        exclude = ['is_delete']


class ShoppingCartSerializer(ModelSerializer):
    commodity_details = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ShoppingCart
        fields = "__all__"

    def validate(self, data):
        if data['number'] <= 0 or data['number'] > data['commodity'].stock:
            raise serializers.ValidationError('number Error')
        return data

    def get_commodity_details(self, shoppingcart):
        return CommoditySerializer(shoppingcart.commodity).data


class OrderGoodsSerializer(ModelSerializer):
    commodity_name = serializers.CharField(source='commodity.name', read_only=True)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    # 得到前端传过来的购物车的商品
    cart = serializers.ListField(write_only=True)
    ordergoods_set = OrderGoodsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['order_id', 'total_count', 'total_amount', 'status', 'user']

    def create(self, validated_data):
        # 订单编号
        user = self.context['request'].user  # self.context['request'] = self.request
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '%06d%02d' % (user.id, random.randint(1, 100))
        # 创建订单信息

        with transaction.atomic():
            # 开启事务，在with中的代码执行完之后自动关闭事务
            # 代码处于一段原子中
            save_point = transaction.savepoint()  # 创建保存点，以免创建订单表不成功却仍然生成
            pay_method = validated_data.get('pay_method')
            try:
                address = Address.objects.get(id=int(validated_data.get('address')))
            except Address.DoesNotExist:
                # transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError('address error')
            address_s = f'{address.province.name} {address.city.name} {address.district.name} {address.place} [{address.receiver} 收] {address.mobile}'
            order = Order.objects.create(
                order_id=order_id,
                total_count=0,
                total_amount=Decimal('0.00'),
                pay_method=pay_method,
                status=1 if pay_method == 1 else 2,
                user=user,
                address=address_s
            )
            try:
                # 获取购物车中药结算的商品
                carts = validated_data.get('cart')
                for cart_id in carts:
                    while True:
                        cart = ShoppingCart.objects.get(id=cart_id)  # 得到要结算的购物车数据
                        commodity = cart.commodity  # 得到购物车对应的商品信息

                        # 原本的库存与销量，开始使用乐观锁
                        origin_stock = commodity.stock
                        origin_sales = commodity.sales

                        # 判断是否超过库存
                        if cart.number > origin_stock:
                            raise serializers.ValidationError('库存不足')
                        # 库存操作：减少库存，增加销量
                        new_stock = origin_stock - cart.number
                        new_sales = origin_sales + cart.number

                        # 修改前对库存进行预先判断,乐观锁操作
                        res = Commodity.objects.filter(stock=origin_stock, id=commodity.id).update(stock=new_stock,
                                                                                                   sales=new_sales)
                        if not res:
                            continue

                        # 创建订单商品数据
                        OrderGoods.objects.create(
                            number=cart.number,
                            price=commodity.price,
                            order=order,
                            commodity=commodity
                        )

                        # 更新订单表
                        order.total_count += cart.number
                        order.total_amount += (cart.number * commodity.price)

                        break
                # 保存订单表的修改
                order.save()
            except Exception as e:
                transaction.savepoint_rollback(save_point)
                raise serializers.ValidationError(e)  # 结束方法 响应给客户数据
            else:
                transaction.savepoint_commit(save_point)

        # 清除购物车已结算的商品数据
        ShoppingCart.objects.filter(id__in=carts).delete()
        return order
