from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from fdfs_client.client import Fdfs_client, get_tracker_conf
import logging

from config.dbs.redisConfig import LOGIN_KEY_TEMPLATE, EXPIRE_TIME
from config.fastdfsConfig import FASTDFS_SERVER_DOMAIN
from users.models import UserDetail
from users.serializers import UserSerializer, UserDetailSerializer
from utils.permission import ActiveUserPermission
from utils.verifyUtil import ImageVerify
import io

tracker_path = get_tracker_conf('utils/fastdfs/client.conf')
Client = Fdfs_client(tracker_path)
logger = logging.getLogger(__name__)

class ImageVerifyView(View):
    """图片验证码视图类"""

    def get(self, request, uuid):
        im = ImageVerify()
        img, code = im.verify_code()
        img_bytes = io.BytesIO()

        img.save(img_bytes, format='png')
        image_bytes = img_bytes.getvalue()

        # 将uuid作为key,将验证码答案作为value缓存到redis数据库中
        cache = get_redis_connection(alias='verify_codes')
        cache.set(LOGIN_KEY_TEMPLATE % uuid, code, EXPIRE_TIME)

        return HttpResponse(image_bytes, content_type='image/png')


# 用户可以查看个人信息和修改个人信息
class UserViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = User.objects.filter(is_active=1)
    serializer_class = UserSerializer
    permission_classes = [ActiveUserPermission]

    def update(self, request, pk):
        # 查询用户得到用户模型对象
        try:
            user = self.get_queryset().get(pk=pk)
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        # 反序列化
        serializer = self.get_serializer(data=request.data, instance=user)
        # 校验
        serializer.is_valid(raise_exception=True)
        # 保存用户信息，修改
        serializer.save()
        # 判断是否有传入详情信息
        user_detail = request.data.get('userdetail')
        if user_detail:
            # 如果有，得到模型对象，修改
            if hasattr(user, 'userdetail'):
                user_detail_serializer = UserDetailSerializer(instance=user.userdetail, data=user_detail)
            else:
                # 没有,创建一个模型对象，保存
                user_detail_serializer = UserDetailSerializer(data=user_detail)
            user_detail_serializer.is_valid(raise_exception=True)
            user_detail_serializer.save()
            serializer.data['userdetail'] = user_detail_serializer
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def avatar(self, request, pk):
        # 获取到该用户
        try:
            user = self.get_queryset().get(pk = pk)
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        # 得到用户上传的文件
        files = request.FILES.get('file')
        # 判断文件类型
        if not files or files.content_type not in ('image/jpeg', 'image/png', 'image/jpg', 'image/gif'):
            return Response(status=HTTP_400_BAD_REQUEST)
        # 获取文件后缀名
        try:
            img_ext_name = files.name.split('.')[-1]
        except Exception as e:
            img_ext_name = 'png'
        # 上传文件到storage,并接受返回结果
        try:
            upload_res = Client.upload_by_buffer(files.read(), file_ext_name=img_ext_name)
        except Exception as e:
            logger.error(f"图片上传出现未知异常{e}")
            return Response(HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            if upload_res.get('Status') != 'Upload successed.':
                logger.error("上传图片失败")
                return Response(HTTP_500_INTERNAL_SERVER_ERROR)

        img_url = FASTDFS_SERVER_DOMAIN + upload_res.get('Remote file_id').decode()
        # 保存图片路径
        if hasattr(user, 'userdetail'):
            user_detail = user.userdetail
            user_detail.avatar = img_url
            user_detail.save()
        else:
            UserDetail.objects.create(user=user, avatar=img_url)
        # 返回图片请求链接
        return Response({'data': img_url})

