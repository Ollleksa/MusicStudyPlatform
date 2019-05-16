from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Lesson
from .serializers import LessonSerializer


class LessonsAPIView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LessonsAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        all_lessons = Lesson.objects.all()
        ser = LessonSerializer(all_lessons, many=True)

        return Response(data=ser.data)

    def post(self, *args, **kwargs):
        ser = LessonSerializer(data=self.request.data)
        if ser.is_valid():
            ser.save()

            return Response(data=ser.data, status=status.HTTP_201_CREATED)
        return Response(data=ser.data, status=status.HTTP_400_BAD_REQUEST)


class OneLessonAPIView(APIView):

    def get(self, *args, **kwargs):
        lesson = Lesson.objects.get(id=kwargs['lesson_id'])
        ser = LessonSerializer(lesson)

        return Response(data=ser.data)