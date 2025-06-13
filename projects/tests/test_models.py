from django.test import TestCase

from projects.models import Project
from users.models import User


class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')

    def test_create_project_model(self):
        self.project = Project.objects.create(
            name='Test Project',
            user=self.user)
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.user, self.project.user)

    def test_delete_project_model(self):
        self.project = Project.objects.create(
            name='Test Project',
            user=self.user)
        self.project.delete()
        self.assertEqual(Project.objects.count(), 0)
