from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from users.forms import SignupForm, ProfileForm
from users.models import User


class UserSignUpFormTestCase(TestCase):
    def test_signup_form(self):
        form_data = {'username': 'XXXX', 'password1': 'ALEX1111!', 'password2': 'ALEX1111!'}
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_password2(self):
        form_data = {'username': 'XXXX', 'password1': 'ALEX1111!', 'password2': 'ALEX1111'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_invalid_password(self):
        form_data = {'username': 'XXXX', 'password1': '1111', 'password2': '1111'}
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProfileFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXX', password='1111')

    def test_profile_form(self):
        form_data = {
            'username': 'XXXX',
            'password1': '1111',
            'password2': 'ALEX11111!',
            'description': 'Example of user description',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_password1(self):
        form_data = {
            'username': 'XXXX',
            'password1': '11111234',
            'password2': 'ALEX11111!',
            'description': 'Example of user description',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_profile_form_invalid_password2(self):
        form_data = {
            'username': 'XXXX',
            'password1': '1111',
            'password2': '1111!',
            'description': 'Example of user description',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
