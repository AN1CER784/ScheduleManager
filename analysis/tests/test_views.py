from django.urls import reverse
from django.test import TestCase

from users.models import User


class AnalysisViewTestCase(TestCase):
    def test_analysis_view(self):
        User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        response = self.client.get(reverse('analysis:summary'))
        self.assertEqual(response.status_code, 200)