from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Lesson
from .serializers import LessonSerializer


class LessonsAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, *args, **kwargs):
        all_lessons = Lesson.objects.all()
        ser = LessonSerializer(all_lessons, many=True)

        return Response(data=ser.data)

    def post(self, *args, **kwargs):
        ser = LessonSerializer(data=self.request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response(data=ser.data, status=status.HTTP_201_CREATED)


class OneLessonAPIView(APIView):

    def get(self, *args, **kwargs):
        lesson = Lesson.objects.get(id=kwargs['lesson_id'])
        ser = LessonSerializer(lesson)

        return Response(data=ser.data)