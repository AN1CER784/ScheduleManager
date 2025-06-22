from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='XXXX', email='test@mail.com', password='1111')

    def test_login_by_username(self):
        response = self.client.post(reverse('users:login'), {'username': 'XXXX', 'password': '1111'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_by_email(self):
        response = self.client.post(reverse('users:login'), {'username': 'test@mail.com', 'password': '1111'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid(self):
        response = self.client.post(reverse('users:login'), {'username': 'XXXX', 'password': '2222'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)


class UserRegisterViewTestCase(TestCase):
    def test_register(self):
        response = self.client.post(reverse('users:signup'),
                                    {'username': 'XXXX', 'email': 'test@mail.com',  'password1': 'LLLL1111', 'password2': 'LLLL1111'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='XXXX').exists())

    def test_register_invalid_password2(self):
        response = self.client.post(reverse('users:signup'),
                                    {'username': 'XXXX', 'email': 'test@mail.com','password1': 'LLLL1111', 'password2': 'LLLL2222'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='XXXX').exists())

    def test_register_invalid_password(self):
        response = self.client.post(reverse('users:signup'),
                                    {'username': 'XXXX', 'email': 'test@mail.com', 'password1': '1111', 'password2': '1111'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='XXXX').exists())


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='XXXX', email='test@mail.com',  password='1111')
        self.client.login(username='XXXX', password='1111')

    def test_profile(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_profile_change(self):
        response = self.client.post(reverse('users:profile'),
                                    {'username': 'XXXX',
                                     'description': 'user description...',
                                     'image': SimpleUploadedFile(name='test_image.jpg',
                                                                 content=open('static/deps/images/baseavatar.jpg',
                                                                              'rb').read(), content_type='image/jpeg')},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='XXXX')
        self.assertEqual(user.description, 'user description...')
        self.assertTrue('test_image' in user.image.name)
        self.assertRedirects(response, reverse('users:profile'))

    def test_profile_change_invalid_password(self):
        response = self.client.post(reverse('users:profile'),
                                    {'username': 'XXXX',
                                     'description': 'user description...',
                                     'image': SimpleUploadedFile(name='test_image.jpg',
                                                                 content=open('static/deps/images/baseavatar.jpg',
                                                                              'rb').read(), content_type='image/jpeg')},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='XXXX')
        self.assertNotEqual(user.description, 'user description...')
        self.assertFalse('test_image' in user.image.name)

    def test_profile_change_invalid_description(self):
        response = self.client.post(reverse('users:profile'),
                                    {'username': 'XXXX', 'password1': '1111', 'password2': '1111',
                                     'description': '123123132',
                                     'image': SimpleUploadedFile(name='test_image.jpg',
                                                                 content=open('static/deps/images/baseavatar.jpg',
                                                                              'rb').read(), content_type='image/jpeg')},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        user = User.objects.get(username='XXXX')
        self.assertTrue(user.check_password('1111'))
        self.assertNotEqual(user.description, '123123132')
        self.assertFalse('test_image' in user.image.name)
