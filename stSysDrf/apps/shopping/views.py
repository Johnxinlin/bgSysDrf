import logging

from django.shortcuts import render

# Create your views here.
from fdfs_client.client import get_tracker_conf, Fdfs_client
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from config.fastdfsConfig import FASTDFS_SERVER_DOMAIN
from shopping.models import Classification, Commodity, CommodityImg, ShoppingCart
from shopping.serializers import ParentClassificationSerializer, CommoditySerializer, ShoppingCartSerializer, \
    OrderSerializer
from utils.permission import TeacherPermission, wrap_permission, create_auto_current_user, update_auto_current_user, \
    destroy_auto_current_user

tracker_path = get_tracker_conf('utils/fastdfs/client.conf')
Client = Fdfs_client(tracker_path)
logger = logging.getLogger(__name__)


class ClassificationViewSet(ModelViewSet):
    queryset = Classification.objects.filter(is_delete=False, parent=None)
    serializer_class = ParentClassificationSerializer
    permission_classes = [IsAuthenticated]

    @wrap_permission(TeacherPermission)
    def create(self, request, *args, **kwargs):
        return ModelViewSet.create(self, request, *args, **kwargs)

    @wrap_permission(TeacherPermission)
    def update(self, request, *args, **kwargs):
        return ModelViewSet.update(self, request, *args, **kwargs)

    @wrap_permission(TeacherPermission)
    def destroy(self, request, *args, **kwargs):
        return ModelViewSet.destroy(self, request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def commodity(self, request, pk):
        classification = Classification.objects.filter(id=pk, is_delete=False).first()
        if not classification:
            return Response(status=HTTP_404_NOT_FOUND)

        classification_attr = 'classification1'
        if classification.parent:
            classification_attr = 'classification2'
        serializer = CommoditySerializer(getattr(classification, classification_attr).filter(is_delete=False),
                                         many=True)
        return Response({'classification': classification.name, 'commodity': serializer.data})


class CommodityViewSet(ModelViewSet):
    """
    商品视图类
    list: 返回所有商品
    create: 创建商品信息
    update: 更新商品信息
    destroy: 删除商品信息
    """
    queryset = Commodity.objects.filter(is_delete=False)
    serializer_class = CommoditySerializer
    permission_classes = [IsAuthenticated]

    @wrap_permission(TeacherPermission)
    def create(self, request, *args, **kwargs):
        return ModelViewSet.create(self, request, *args, **kwargs)

    @wrap_permission(TeacherPermission)
    def update(self, request, *args, **kwargs):
        return ModelViewSet.update(self, request, *args, **kwargs)

    @wrap_permission(TeacherPermission)
    def destroy(self, request, *args, **kwargs):
        return ModelViewSet.destroy(self, request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def img(self, request, pk):
        """
        上传商品图像
        :param request:
        :param pk:
        :return:
        """
        try:
            commodity = self.get_queryset().get(id=pk)
        except Commodity.DoesNotExist:
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

        if hasattr(commodity, 'commodityimg_set'):
            commodityimg = commodity.commodityimg_set
            commodityimg.src = img_url
            commodityimg.save()
        else:
            CommodityImg.objects.create(src=img_url, commodity=commodity)
        return Response({'data': img_url})

    @action(methods=['get'], detail=False)
    def optimization(self, request):
        commodities = self.get_queryset().order_by('-comments').order_by('-create_time')
        if len(commodities) > 5:
            commodities = commodities[0:5]
        serializer = self.get_serializer(commodities, many=True)
        return Response(serializer.data)


class ShoppingCartViewSet(ModelViewSet):
    """
    购物车视图类
    create: 创建商品购物车
    list: 查询所有商品购物车
    retrieve: 查询商品购物车
    destroy: 删除商品购物车
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.shoppingcart_set.all()

    @create_auto_current_user
    def create(self, request, *args, **kwargs):
        return ModelViewSet.create(self, request, *args, **kwargs)

    @update_auto_current_user
    def update(self, request, *args, **kwargs):
        return ModelViewSet.update(self, request, *args, **kwargs)

    @destroy_auto_current_user
    def destroy(self, request, *args, **kwargs):
        return ModelViewSet.destroy(self, request, *args, **kwargs)


class OrderViewSet(ReadOnlyModelViewSet, CreateModelMixin):
    """
    订单表视图类
    create: 创建订单，同时删除购物车
    list: 查看所有订单
    retrieve: 查看订单
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.order_set.all()
