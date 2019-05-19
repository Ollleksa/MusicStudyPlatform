from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from .models import Lesson
from .serializers import LessonSerializer


class ApiTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='oleksa', email='test@test.test', password='Some11Pass')
        self.other_user = User.objects.create_user(username='new', email='ole@ole.ole', password='Some11Pass')
        self.new_lesson = Lesson(author=self.user, title='Test', content='Test content')
        self.new_lesson.save()
        self.new_lesson.likes.add(self.user, self.other_user)

    def test_get_all_lessons(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            reverse('api_lessons'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_not_auth(self):
        resp = self.client.get(
            reverse('api_lessons'),
        )
        self.assertEqual(resp.status_code, 401)

    def test_get_one_lesson(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            '/api/lesson/{}'.format(self.new_lesson.id),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_404_lesson(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            '/api/lesson/{}'.format(self.new_lesson.id + 10),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 404)

    def test_lesson_creation(self):
        token = AccessToken.for_user(self.user)
        data = {'title': 'New_test', 'content': 'Test_content'}
        resp = self.client.post(
            reverse('lesson'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}',
            data=data,
        )
        self.assertEqual(resp.status_code, 200)

    def test_lesson_creation_fail(self):
        token = AccessToken.for_user(self.user)
        data = {'title': '', 'content': 'Test_content'}
        resp = self.client.post(
            reverse('lesson'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}',
            data=data,
        )
        self.assertEqual(resp.status_code, 400)

    def test_deletion(self):
        token = AccessToken.for_user(self.user)
        self.assertTrue(Lesson.objects.filter(id = self.new_lesson.id).exists())
        resp = self.client.delete(
            '/api/lesson/{}'.format(self.new_lesson.id),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertTrue(not Lesson.objects.filter(id = self.new_lesson.id).exists())
        self.assertEqual(resp.status_code, 204)

    def test_deletion_non_author(self):
        new_user = get_user_model().objects.create_user(username='new_one', email='test2@tt.test', password='Some11Pass')
        token = AccessToken.for_user(new_user)
        self.assertTrue(Lesson.objects.filter(id = self.new_lesson.id).exists())
        resp = self.client.delete(
            '/api/lesson/{}'.format(self.new_lesson.id),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertTrue(Lesson.objects.filter(id = self.new_lesson.id).exists())
        self.assertEqual(resp.status_code, 403)

    def test_patch_lesson(self):
        token = AccessToken.for_user(self.user)
        data = {'content': 'Patched content'}
        resp = self.client.patch(
            '/api/lesson/{}'.format(self.new_lesson.id),
            data=data,
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Lesson.objects.get(id=self.new_lesson.id).content, 'Patched content')

    def test_get_likes(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            '/api/lesson/{}/likes'.format(self.new_lesson.id),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        print(resp.data)
        self.assertEqual(resp.status_code, 200)