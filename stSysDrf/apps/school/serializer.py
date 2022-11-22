# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: serializer.py
@time: 2022/11/18 21:51
"""
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import *


class ClassesSerializer(serializers.ModelSerializer):
    memberDetail = serializers.SerializerMethodField()  # 会调用get_属性名的方法，传入当前的模型对象，把返回值赋值给这个属性

    class Meta:
        model = Classes
        exclude = ['is_delete']

    def get_memberDetail(self, classes):
        serializer = UserSerializer(classes.member.all(), many=True)
        data = {
            'teacher:': [i for i in serializer.data if i['is_superuser'] or i['is_staff'] or 1 in i['groups']],
            'students': [i for i in serializer.data if 2 in i['groups']]
        }
        return data
