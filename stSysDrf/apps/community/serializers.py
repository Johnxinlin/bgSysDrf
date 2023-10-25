# encoding: utf-8 
"""
@version: v1.0
@author: ligui
@contact: 1947346653@qq.com
@software: PyCharm
@file: serializers.py
@time: 2022/12/1 20:17
"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from community.models import Article, Comment


class ArticleSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    label_name = serializers.CharField(source='label.name', read_only=True)
    user_avatar = serializers.CharField(source='user.userdetail.avatar', read_only=True)

    class Meta:
        model = Article
        exclude = ['is_delete']


class SonCommentSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.userdetail.avatar', read_only=True)
    reply_username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_reply_username(self, comment):
        name = Comment.objects.get(id=comment.reply_comment).user.username
        return name


class CommentSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.userdetail.avatar', read_only=True)
    sonComments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_sonComments(self, comment):
        sonComments = Comment.objects.filter(parent_comment=comment.id)
        serializer = SonCommentSerializer(sonComments, many=True)
        data = serializer.data
        data.reverse()
        return data
