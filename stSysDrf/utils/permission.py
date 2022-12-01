# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: permission.py
@time: 2022/11/19 15:00
"""
from functools import update_wrapper

from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from work.models import Label, Topic


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


class ActiveUserPermission(BasePermission):
    """当前激活的用户权限类"""

    def has_permission(self, request, view):
        # 操作的用户是否是当前登陆的用户
        user = request.user
        return user.id == int(view.kwargs['pk'])


class LabelUpdateOrDeletePermission(BasePermission):
    """题目标签名更新或删除权限类"""

    def has_permission(self, request, view):
        user = request.user
        try:
            label = Label.objects.get(pk=view.kwargs['pk'])
        except Label.DoesNotExist:
            return Response(status=HTTP_204_NO_CONTENT, data={'msg': '删除成功'})
        return user == label.user or user.is_superuser


class TopicUpdateOrDeletePermission(BasePermission):
    """题目标签名更新或删除权限类"""

    def has_permission(self, request, view):
        user = request.user
        try:
            topic = Topic.objects.get(pk=view.kwargs['pk'])
        except Topic.DoesNotExist:
            return Response(status=HTTP_204_NO_CONTENT, data={'msg': '删除成功'})
        return user == topic.user or user.is_superuser


def wrap_permission(*permissions, validate_permission=True):
    """
    视图方法权限限定装饰器
    :param permissions: 权限类
    :param validate_permission: 是否校验权限
    :return:
    """

    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            self.permission_classes = permissions
            if validate_permission:
                self.check_permissions(request)
            return func(self, request, *args, **kwargs)

        # return update_wrapper(wrapper, func)
        return wrapper

    return decorator


def create_auto_current_user(func):
    def f(self, request, *args, **kwargs):
        request.POST._mutable = True  # 让请求参数可以修改
        request.data['user'] = request.user.id
        return func(self, request, *args, **kwargs)

    return f
