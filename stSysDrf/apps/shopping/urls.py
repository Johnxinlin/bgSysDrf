# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: urls.py
@time: 2022/12/3 16:50
"""
from rest_framework.routers import DefaultRouter

from shopping.views import ClassificationViewSet, CommodityViewSet, ShoppingCartViewSet, OrderViewSet, PaymentViewSet

urlpatterns = []
router = DefaultRouter()
router.register("classification", ClassificationViewSet)
router.register("commodity", CommodityViewSet)
router.register("cart", ShoppingCartViewSet, basename='shoppingcart')
router.register("order", OrderViewSet, basename='order')
router.register("payment", PaymentViewSet)
urlpatterns += router.urls
