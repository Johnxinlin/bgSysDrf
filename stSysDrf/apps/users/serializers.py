# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: serializers.py
@time: 2022/11/19 15:24
"""
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import UserDetail


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'
        extra_kwargs = {
            'avatar': {'read_only': True},
            'user': {'write_only': True}
        }


class UserSerializer(ModelSerializer):
    userdetail = UserDetailSerializer(required=False, read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'last_name', 'user_permissions']
        extra_kwargs = {
            'last_login': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'groups': {'read_only': True},
        }
