from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from users.forms import SignupForm, ProfileForm
from users.models import User, Company


class UserSignUpFormTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_signup_form(self):
        request = self.factory.get("/")
        request.LANGUAGE_CODE = "en"
        form_data = {'username': 'XXXX', 'email': 'testmail@mail.com', 'password1': 'ALEX1111!',
                     'password2': 'ALEX1111!', 'company_name': 'Acme'}
        form = SignupForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_password2(self):
        request = self.factory.get("/")
        request.LANGUAGE_CODE = "en"
        form_data = {'username': 'XXXX', 'email': 'testmail@mail.com', 'password1': 'ALEX1111!',
                     'password2': 'ALEX1111', 'company_name': 'Acme'}
        form = SignupForm(data=form_data, request=request)
        self.assertFalse(form.is_valid())

    def test_signup_form_invalid_password(self):
        request = self.factory.get("/")
        request.LANGUAGE_CODE = "en"
        form_data = {'username': 'XXXX', 'email': 'testmail@mail.com', 'password1': '1111', 'password2': '1111',
                     'company_name': 'Acme'}
        form = SignupForm(data=form_data, request=request)
        self.assertFalse(form.is_valid())


class ProfileFormTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name="Acme")
        self.user = User.objects.create_user(username='XXXX', password='1111', email='testmail@mail.com',
                                             company=company)

    def test_profile_form(self):
        form_data = {
            'username': 'XXXX',
            'password1': '1111',
            'password2': 'ALEX11111!',
            'email': 'testmail@mail.com',
            'description': 'Example of user description',
            'image': SimpleUploadedFile(name='test_image.jpg',
                                        content=open('static/deps/images/baseavatar.jpg',
                                                     'rb').read(), content_type='image/jpeg')
        }

        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
