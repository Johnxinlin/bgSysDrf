import random

from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from utils.permission import TeacherPermission, LabelUpdateOrDeletePermission, create_auto_current_user, \
    TopicUpdateOrDeletePermission
from work.models import Label, Topic
from work.serializers import LabelSerializer, TopicSerializer, TopicStudentSerializer
from utils.permission import wrap_permission
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
import elasticsearch
from elasticsearch import Elasticsearch
from config.elasticsearchConfig import *

# Create your views here.

es = Elasticsearch([{'host': HOST, 'port': PORT}], timeout=3600)


class TopicPaginationPageNumber(PageNumberPagination):
    page_size_query_param = 'size'  # 指定每页条数的字段名为size
    max_page_size = 100  # 每页最大条数
    page_size = 3  # 每页默认条数


class TopicPaginationLimitOffset(LimitOffsetPagination):
    default_limit = 3  # 指定默认每次查询多少条数据
    max_limit = 3


class LabelViewSet(ModelViewSet):
    # 权限： 1.查询：登陆及以上 2. 创建标签： 老师及以上 3. 修改标签：所有者及超级管理员 4. 删除标签： 所有者和超级管理员
    permission_classes = [IsAuthenticated]
    serializer_class = LabelSerializer
    queryset = Label.objects.all()

    @wrap_permission(TeacherPermission)
    @create_auto_current_user
    def create(self, request, *args, **kwargs):
        # # 将当前登陆的用户id传入
        # request.POST._mutable = True  # 让请求参数可以修改
        # request.data['user'] = request.user.id
        return ModelViewSet.create(self, request, *args, **kwargs)

    @wrap_permission(LabelUpdateOrDeletePermission)
    def update(self, request, *args, **kwargs):
        return ModelViewSet.update(self, request, *args, **kwargs)

    @wrap_permission(LabelUpdateOrDeletePermission)
    def destroy(self, request, *args, **kwargs):
        return ModelViewSet.destroy(self, request, *args, **kwargs)


class TopicViewSet(ModelViewSet):
    """
    题目视图集
    功能：出题，修改题，查看所有题，顺序刷题，考试题，模拟测试（随机题）
    """
    # 权限： 1.查询：登陆及以上 2.创建题目：老师及以上 3.更新题目：所有者及超级管理员 4.删除题目：所有者及超级管理员
    permission_classes = [IsAuthenticated]
    queryset = Topic.objects.filter(is_delete=False)
    serializer_class = TopicSerializer
    pagination_class = TopicPaginationLimitOffset

    def get_serializer(self, *args, **kwargs):
        # 答案不返回给学生
        if self.action in ['noanswer', 'random', 'exam']:
            return TopicStudentSerializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        # 考试题不展示给学生
        if self.action in ['noanswer', 'random']:
            return Topic.objects.filter(~Q(label__name__contains="考试") & Q(is_delete=False))
        return self.queryset

    @wrap_permission(TeacherPermission)
    @create_auto_current_user
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        es.index(index='topic', id=res_data['id'], body=res_data)
        return Response(res_data)

    @wrap_permission(TopicUpdateOrDeletePermission)
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data['user'] = request.user.id

        try:
            topic = self.get_queryset().get(id=kwargs['pk'])
        except Topic.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(topic, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res_data = serializer.data
        es.update(index='topic', id=res_data['id'], body={"doc":res_data})
        return Response(res_data)

    @wrap_permission(TeacherPermission)
    def list(self, request, *args, **kwargs):
        return ModelViewSet.list(self, request, *args, **kwargs)

    @wrap_permission(TeacherPermission)
    def retrieve(self, request, *args, **kwargs):
        return ModelViewSet.retrieve(self, request, *args, **kwargs)

    @wrap_permission(TopicUpdateOrDeletePermission)
    def destroy(self, request, *args, **kwargs):
        res_data = ModelViewSet.destroy(self, request, *args, **kwargs)
        es.delete(index='topic', id=kwargs['pk'])
        return res_data

    @action(methods=['get'], detail=False)
    def noanswer(self, request):
        return ModelViewSet.list(self, request)

    @action(methods=['get'], detail=True)
    def exam(self, request, pk):
        """
        查询指定标签对应的考试题
        :param request:
        :param pk: 指定标签id
        :return:
        """
        topic = Topic.objects.filter(label_id=pk, is_delete=False, label__name__contains="考试")
        serializer = self.get_serializer(topic, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def random(self, request):
        try:
            size = int(request.query_params.get('size', 3))
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            data = random.sample(list(self.get_queryset()), int(size))
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST, data={'msg': '超出题目总数'})
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def inites(self, request):
        topics = self.get_queryset()
        serializer = self.get_serializer(topics, many=True)
        data = serializer.data

        for i in data:
            es.index(index='topic', id=i['id'], body=i)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def search(self, request):
        """
        题目搜索，学生只能查询到题目，教师可查询到题目和答案
        :param request:
        :return:
        """
        data = dict(request.query_params)
        offset = int(data.get('offset', [0])[0])  # 如果offset未传值，则默认为0，get取得的值为列表，故默认为元素为0的列表
        limit = int(data.get('limit', [3])[0])
        subject = data.get('subject', [''])[0]

        # query = {
        #     "query": {
        #         "match": {
        #             "subject": subject
        #         }
        #     },
        #     "highlight": {
        #         "pre_tags": "<span class='s-key' >",
        #         "post_tags": "</span>",
        #         "fields": {
        #             "subject": {}
        #         }
        #     },
        #     "from": offset,
        #     "size": limit
        # }

        # 权限限定，除老师及超级管理员外不可查询答案


        query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "subject": subject
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "pre_tags": "<span style='color:red;'>",
                "post_tags": "</span>",
                "fields": {
                    "subject": {}
                }
            },
            "from": offset,
            "size": limit
        }

        user = request.user
        groups = user.groups.all()
        group = Group.objects.filter(name="老师")[0]
        worker = (group in groups or request.user.is_superuser)
        if not worker:
            query['_source'] = {
                'excludes': ['answer']
            }
            if subject:
                # 搜索指定得题目
                query['query']['bool'] = {
                    "must_not": [
                        {
                            "match_phrase": {
                                "label_name": "考试"
                            }
                        }
                    ],
                    "should": [
                        {
                            "match": {
                                "subject": subject
                            }
                        }
                    ]
                }

            else:
                # 搜索所有
                query['query']['bool'] = {
                    "must_not": [
                        {
                            "match_phrase": {
                                "label_name": "考试"
                            }
                        }
                    ],
                    "should": [
                        {
                            "match_all": {}
                        }
                    ]
                }
        else:
            query['query']['bool']['should'].append({"match_all": {}})

        try:
            es_res = es.search(index='topic', body=query)
            count = es_res['hits']['total']['value']
            subject_url = f'subject={subject}' if subject else ''
            next = rf'{CLIENT}/work/topics/search/?{subject_url}limit={limit}&offset={offset + limit}' if offset + limit < count else None
            previous = rf'{CLIENT}/work/topics/search/?{subject_url}limit={limit}&offset={offset - limit}' if offset > 0 else None
            results = [self.highlight(i) for i in es_res['hits']['hits']]
            res = {
                "count": count,
                "next": next,
                "previous": previous,
                "results": results
            }
        except elasticsearch.exceptions.NotFoundError:
            res = {
                "count": 0,
                "next": None,
                "previous": None,
                "results": []
            }
        return Response(res)

    # 配置高亮函数
    def highlight(self, i):
        if i.get('highlight'):
            i['_source']['subject'] = i['highlight']['subject'][0]
            return i['_source']
        return i['_source']
