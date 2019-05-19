from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Lesson, Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user',)
        read_only_fields = ('user',)


class LessonSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), default=CurrentUserDefault())
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'author', 'title', 'content', 'timestamp', 'likes')
        read_only_fields = ('id', 'timestamp')

