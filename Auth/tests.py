from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings


from .models import PlatformUser


class UserCreationTestCase(TestCase):
    def setUp(self):
        self.name = 'test'
        self.email = 'test@test.test'
        self.pword = 'Some11pass'

    def test_create_user_success(self):
        PlatformUser.objects.create_user(username=self.name, email=self.email, password=self.pword)
        self.assertTrue(PlatformUser.objects.filter(username=self.name).exists())

    def test_create_superuser_success(self):
        PlatformUser.objects.create_superuser(username=self.name, email=self.email, password=self.pword)
        self.assertTrue(PlatformUser.objects.get(username=self.name).is_admin)


class LogInOut(TestCase):
    def setUp(self):
        self.c = Client()
        self.name = 'test'
        self.email = 'test@test.test'
        self.pword = 'Some11pass'
        PlatformUser.objects.create_user(username='oleksa', email='let@it.be', password='some11pass')

    def test_login(self):
        response = self.c.post('/auth/login/', {'username': 'oleksa', 'password': 'some11pass'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)


class APITestUser(APITestCase):

    def setUp(self):
        self.name, self.email, self.password = "oleks", "test@test.test", "11testes"
        self.user = PlatformUser.objects.create_user(self.name, self.email, self.password)

    def test_auth(self):
        data ={"username": self.name, "password": self.password}
        resp = self.client.post(reverse("token_obtain_pair"), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_auth_refresh(self):
        data = {"username": self.name, "password": self.password}
        resp = self.client.post(reverse("token_obtain_pair"), data=data)
        resp = self.client.post(reverse('token_refresh'), data={"refresh": resp.data["refresh"]})
        self.assertEqual(resp.status_code, 200)

    def test_get_all_user_info(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            reverse('all_users'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)

    def test_get_user_info(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.get(
            reverse('user'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 200)

    def test_delete_user_by_api(self):
        token = AccessToken.for_user(self.user)
        resp = self.client.delete(
            reverse('user'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}'
        )
        self.assertEqual(resp.status_code, 204)
        self.assertTrue(not PlatformUser.objects.filter(username=self.name).exists())

    def test_create_user_by_api(self):
        self.user.is_admin = True
        self.user.save()
        token = AccessToken.for_user(self.user)
        data = {"username": "new_name", "email": "real@mail.com", "password": self.password}
        resp = self.client.post(
            reverse('all_users'),
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[1]} {token}',
            data=data
        )
        self.assertTrue(PlatformUser.objects.filter(username="new_name").exists())

    def test_update_user(self):
        token = AccessToken.for_user(self.user)
        pass

    def test_sign_up(self):
        data = {"username": "new_name", "email": "real@mail.com", "password": self.password}
        resp = self.client.post(
            reverse('sign_up'),
            data=data
        )
        self.assertTrue(PlatformUser.objects.filter(username="new_name").exists())