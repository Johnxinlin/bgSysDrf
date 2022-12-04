# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: urls.py.py
@time: 2022/12/1 20:22
"""
from rest_framework.routers import DefaultRouter

from community.views import ArticleViewSet, CommentViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register('article', ArticleViewSet)
router.register('comment', CommentViewSet)
urlpatterns += router.urls