import random
import string

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from celery_tasks.email.tasks import send_mail_task
from .serializer import *
from utils.permission import *
from rest_framework.viewsets import ViewSet


# Create your views here.
class ClassesViewSet(ModelViewSet):
    permission_classes = [TeacherPermission]
    queryset = Classes.objects.filter(is_delete=False)
    serializer_class = ClassesSerializer

    @action(methods=['post'], detail=True)
    def add_student(self, request, pk):
        # 给班级添加成员
        # 获取指定的班级
        try:
            classes = Classes.objects.get(pk = pk)
        except Classes.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)
        # 判断该成员是否已经属于该班级
        username = request.data.get('username')
        member = classes.member.filter(username=username)
        if member:
            # 属于
            return Response({'msg': '该用户已经添加到该班级'})
        else:
            # 不属于， 判断是否存在该用户
            user = User.objects.filter(username=username).first()
            if user:
                # 存在，user表中有用户信息，但是没有加入到这个班级
                # 添加到该班级
                classes.member.add(user)
                return Response(self.get_serializer(user).data)
            else:
                # 不存在，没有该用户
                # 创建，再添加到该班级
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                # 创建用户
                username = request.data.get('username')
                email = request.data.get('email')
                firstname = request.data.get('first_name')
                user = User(username=username, first_name=firstname, email=email)
                # 设置随机密码

                source = string.ascii_letters + string.digits
                password = ''.join(random.sample(source, 6))
                user.set_password(password)
                user.save()

                # 用户分组并加入班级
                group_student = Group.objects.get(id=2)
                group_student.user_set.add(user)
                classes.member.add(user)

                # 使用celery发送邮件通知, 异步处理
                send_mail_task.delay(email, user.username, classes.name, password)
                return Response(serializer.data, status=HTTP_201_CREATED)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'add_student':
            return CreateUserSerializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)






