# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: urls.py
@time: 2022/11/29 13:01
"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from work.views import LabelViewSet, TopicViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register('label', LabelViewSet)
router.register('topics', TopicViewSet)
urlpatterns += router.urls
