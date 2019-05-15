from django.test import TestCase, Client

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
