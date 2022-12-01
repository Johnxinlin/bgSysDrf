# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: urls.py
@time: 2022/11/19 17:40
"""
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from users.views import ImageVerifyView, UserViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('image/verifiaction/<uuid:uuid>', ImageVerifyView.as_view()),
    path('login/', obtain_jwt_token),
]
router = DefaultRouter()
router.register('users', UserViewSet)
urlpatterns += router.urls
