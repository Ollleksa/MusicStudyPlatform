from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Lesson, Like


class LikeSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), default=CurrentUserDefault())
    # lesson = serializers.RelatedField(source='lessons', queryset=Lesson.objects.all())

    class Meta:
        model = Like
        fields = ('user', 'lesson')


class LessonSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), default=CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = ('id', 'author', 'title', 'content', 'timestamp')
        read_only_fields = ('id', 'timestamp')

