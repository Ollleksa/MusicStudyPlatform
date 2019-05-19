from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Lesson
from .serializers import LessonSerializer, LikeSerializer


class LessonViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, lesson_id=None):
        queryset = Lesson.objects.all()
        lesson = get_object_or_404(queryset, id=lesson_id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def create(self, request):
        ser = LessonSerializer(data=self.request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def delete(self, request, lesson_id=None):
        queryset = Lesson.objects.all()
        lesson = get_object_or_404(queryset, id=lesson_id)
        if lesson.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, lesson_id=None):
        queryset = Lesson.objects.all()
        lesson = get_object_or_404(queryset, id=lesson_id)
        if lesson.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        ser = LessonSerializer(lesson, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class LikeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, lesson_id=None):
        queryset = Lesson.objects.all()
        lesson = get_object_or_404(queryset, id=lesson_id)
        likes = lesson.likes.all()
        print(likes)
        ser = LikeSerializer(likes, many=True)
        print(ser.data)
        return Response(ser.data)