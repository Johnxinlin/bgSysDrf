from django.db.models import F
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

# Create your views here.
from community.models import Article, Comment
from community.serializers import ArticleSerializer, CommentSerializer
from utils.permission import create_auto_current_user, wrap_permission, ArticleUpdateOrDeletePermission, \
    CommentDeletePermission
from rest_framework.pagination import PageNumberPagination


class ArticlePaginationPageNumber(PageNumberPagination):
    page_size_query_param = 'size'
    page_size = 10
    max_page_size = 100


class ArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(is_delete=False, status=1)
    permission_classes = [IsAuthenticated]
    pagination_class = ArticlePaginationPageNumber

    def get_queryset(self):
        if self.action in ['update', 'destroy']:
            return Article.objects.filter(is_delete=False)
        return self.queryset

    @create_auto_current_user
    def create(self, request, *args, **kwargs):
        return ModelViewSet.create(self, request, *args, **kwargs)

    @wrap_permission(ArticleUpdateOrDeletePermission)
    def update(self, request, *args, **kwargs):
        return ModelViewSet.update(self, request, *args, **kwargs)

    @wrap_permission(ArticleUpdateOrDeletePermission)
    def destroy(self, request, *args, **kwargs):
        return ModelViewSet.destroy(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        Article.objects.filter(id=kwargs['pk']).update(page_view=F('page_view') + 1)
        return ModelViewSet.retrieve(self, request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def comment(self, request, pk):
        comments = Comment.objects.filter(article_id=pk, level=1)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @create_auto_current_user
    def create(self, request, *args, **kwargs):
        return CreateModelMixin.create(self, request, *args, **kwargs)

    @wrap_permission(CommentDeletePermission)
    def destroy(self, request, *args, **kwargs):
        return DestroyModelMixin.destroy(self, request, *args, **kwargs)