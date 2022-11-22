# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: permission.py
@time: 2022/11/19 15:00
"""
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


class TeacherPermission(BasePermission):
    """教师权限类"""

    def has_permission(self, request, view):
        user = request.user  # 获取请求中用户的信息
        # 获取有权限身份 - 组
        group = Group.objects.filter(name='老师')[0]
        # 判断当前登陆的用户有没有这个组
        groups = user.groups.all()
        # 超级管理员与老师分组的都给予权限
        return user.is_superuser or group in groups
