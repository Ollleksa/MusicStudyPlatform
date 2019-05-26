from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from .models import Request


class RequestApiTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='oleksa', email='test@test.test', password='Some11Pass')
        self.other_user = User.objects.create_user(username='new', email='ole@ole.ole', password='Some11Pass')
        self.new_request = Request(requester=self.user, agent=self.other_user, title='Test', content='Test content')
        self.new_request.save()

    def test_get_all_requests(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            reverse('api_requests'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_one_request(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            reverse('one_request', kwargs={'request_id': self.new_request.id}),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_404_request(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            reverse('one_request', kwargs={'request_id': self.new_request.id+10}),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 404)

    def test_request_creation(self):
        token = AccessToken.for_user(self.user)
        data = {'agent': self.other_user.username, 'title': 'New_test', 'content': 'Test_content'}
        resp = self.client.post(
            reverse('request'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}',
            data=data,
        )
        self.assertEqual(resp.status_code, 200)

    # def test_request_creation_fail(self):
    #     token = AccessToken.for_user(self.user)
    #     data = {'title': '', 'content': 'Test_content'}
    #     resp = self.client.post(
    #         reverse('request'),
    #         HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}',
    #         data=data,
    #     )
    #     self.assertEqual(resp.status_code, 400)

    def test_deletion(self):
        token = AccessToken.for_user(self.user)
        self.assertTrue(Request.objects.filter(id = self.new_request.id).exists())
        resp = self.client.delete(
            reverse('one_request', kwargs={'request_id': self.new_request.id}),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertTrue(not Request.objects.filter(id = self.new_request.id).exists())
        self.assertEqual(resp.status_code, 204)

    def test_deletion_non_author(self):
        new_user = get_user_model().objects.create_user(username='new_one', email='test2@tt.test', password='Some11Pass')
        token = AccessToken.for_user(new_user)
        self.assertTrue(Request.objects.filter(id = self.new_request.id).exists())
        resp = self.client.delete(
            reverse('one_request', kwargs={'request_id': self.new_request.id}),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertTrue(Request.objects.filter(id = self.new_request.id).exists())
        self.assertEqual(resp.status_code, 403)

    def test_patch_request(self):
        token = AccessToken.for_user(self.user)
        data = {'content': 'Patched content'}
        resp = self.client.patch(
            reverse('one_request', kwargs={'request_id': self.new_request.id}),
            data=data,
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Request.objects.get(id=self.new_request.id).content, 'Patched content')