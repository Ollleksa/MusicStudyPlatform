from rest_framework import serializers

from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'author', 'title', 'content', 'timestamp')
        read_only_fields = ('id', 'timestamp')