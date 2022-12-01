# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: serializers.py
@time: 2022/11/29 13:22
"""
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from work.models import Label, Topic



class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        # exclude = ['user']
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    label_name = serializers.CharField(source='label.name', read_only=True)
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Topic
        exclude = ['is_delete', 'create_time', 'update_time']



class TopicStudentSerializer(ModelSerializer):
    label_name = serializers.CharField(source='label.name', read_only=True)
    author = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Topic
        exclude = ['is_delete', 'create_time', 'update_time', 'answer']


