from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import User


class UserViewTestCase(TestCase):
    def test_login(self):
        User.objects.create_user(username='XXXX', password='1111')
        response = self.client.post(reverse('users:login'), {'username': 'XXXX', 'password': '1111'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_signup(self):
        response = self.client.post(reverse('users:signup'),
                                    {'username': 'Alex', 'password1': 'ALEX1111!', 'password2': 'ALEX1111!'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_change_profile(self):
        user = User.objects.create_user(username='XXXX', password='1111')
        self.client.login(username='XXXX', password='1111')
        response = self.client.post(reverse('users:profile'),
                                    {'username': 'XXXXXXXX', 'password1': '1111', 'password2': 'ALEX1111!', 'description': 'user description...', 'image': SimpleUploadedFile(name='test_image.jpg', content=open('static/deps/images/baseavatar.jpg', 'rb').read(), content_type='image/jpeg')},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        user.refresh_from_db()
        self.assertEqual(user.username, 'XXXXXXXX')
        self.assertTrue(user.check_password('ALEX1111!'))
        self.assertEqual(user.description, 'user description...')
        self.assertTrue('test_image' in user.image.name)

    def test_logout(self):
        User.objects.create_user(username='XXXX', password='1111')
        self.client.login(username='XXXX', password='1111')
        response = self.client.post(reverse('users:logout'), follow=True)
        self.assertRedirects(response, reverse('users:login'))
        self.assertFalse(response.context['user'].is_authenticated)

