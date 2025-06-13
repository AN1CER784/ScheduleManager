from django.urls import reverse
from django.test import TestCase

from projects.models import Project
from users.models import User


class ProjectViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')

    def test_add_project(self):
        response = self.client.post(reverse('projects:add_proj'), {'name': 'My test project'})
        self.assertEqual(response.status_code, 200)
        project = Project.objects.first()
        self.assertIsNotNone(project)
        self.assertEqual(project.name, 'My test project')
        self.assertEqual(project.user, self.user)

    def test_edit_project(self):
        project = Project.objects.create(name='My test project', user=self.user)
        response = self.client.post(reverse('projects:edit_proj'), {'name': 'My test project edited', 'project_id': project.id})
        self.assertEqual(response.status_code, 200)
        project = Project.objects.first()
        self.assertIsNotNone(project)
        self.assertEqual(project.name, 'My test project edited')
        self.assertEqual(project.user, self.user)

    def test_del_project(self):
        project = Project.objects.create(name='My test project', user=self.user)
        response = self.client.post(reverse('projects:del_proj'), {'project_id': project.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.count(), 0)
