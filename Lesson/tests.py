from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Lesson
from .serializers import LessonSerializer


class ApiTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        us = User.objects.create_user(username='oleksa', email='test@test.test', password='Some11Pass')
        self.new_lesson = Lesson(author=us, title='Test', content='Test content')
        self.new_lesson.save()

    def test_serializer(self):
        ser = LessonSerializer(instance=self.new_lesson)
        print(ser.data)
