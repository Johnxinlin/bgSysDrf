# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: serializers.py
@time: 2022/11/19 15:24
"""
import re

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import UserDetail, Area, Address


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


class AreaSerializer(ModelSerializer):
    """区划自身序列化器"""

    class Meta:
        model = Area
        fields = ['id', 'name']


class ParentSerializer(ModelSerializer):
    """区划自身及子级区划序列化器"""
    area_set = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'area_set']


class AddressSerializer(ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Address
        exclude = ['is_delete']

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式错误')
        return value
