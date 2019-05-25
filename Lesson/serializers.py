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


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'avatar')


class LessonSerializer(serializers.ModelSerializer):
    #author = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), default=CurrentUserDefault())
    author = AuthorSerializer(many=False, required=False)

    class Meta:
        model = Lesson
        fields = ('id', 'author', 'title', 'content', 'header_image', 'timestamp')
        read_only_fields = ('id', 'timestamp')

    def create(self, validated_data):
        lesson = Lesson(**validated_data)
        lesson.author = self.context['request'].user
        lesson.save()
        return lesson