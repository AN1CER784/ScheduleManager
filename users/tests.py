from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .forms import SignupForm, ProfileForm
from .models import User


class UserViewsTestCase(TestCase):
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
                                    {'username': 'XXXXXXXX', 'password1': '1111', 'password2': 'ALEX1111!',
                                     'description': 'user description...',
                                     'image': SimpleUploadedFile(name='test_image.jpg',
                                                                 content=open('static/deps/images/baseavatar.jpg',
                                                                              'rb').read(), content_type='image/jpeg')},
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
        self.assertEqual(response.status_code, 200)


class UserFormsTestCase(TestCase):
    def test_signup_form(self):
        form_data = {'username': 'XXXX', 'password1': 'ALEX1111!', 'password2': 'ALEX1111!'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form_data = {'username': 'XXXX', 'password1': 'ALEX1111!', 'password2': 'ALEX1111'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form(self):
        user = User.objects.create_user(username='XXXX', password='1111')

        form_data = {
            'username': 'XXXX',
            'password1': '1111',
            'password2': 'ALEX11111!',
            'description': 'user description...',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_password1(self):
        user = User.objects.create_user(username='XXXX', password='1111')

        form_data = {
            'username': 'XXXX',
            'password1': '11111234',
            'password2': 'ALEX11111!',
            'description': 'user description...',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())

    def test_profile_form_invalid_password2(self):
        user = User.objects.create_user(username='XXXX', password='1111')

        form_data = {
            'username': 'XXXX',
            'password1': '1111',
            'password2': '1111!',
            'description': 'user description...',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
