from django.test import TestCase

from projects.models import Project
from users.models import User, Company


class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Acme")
        self.user = User.objects.create_user(username='user', password='pass', company=self.company)

    def test_create_project_model(self):
        project = Project.objects.create(name='Test Project', company=self.company, created_by=self.user)
        project.participants.add(self.user)
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(self.company, project.company)

    def test_delete_project_model(self):
        project = Project.objects.create(name='Test Project', company=self.company, created_by=self.user)
        project.delete()
        self.assertEqual(Project.objects.count(), 0)
