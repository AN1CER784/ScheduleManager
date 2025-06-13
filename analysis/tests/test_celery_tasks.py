from unittest.mock import patch

from django.test import TestCase
from analysis.tasks import make_day_summary, make_week_summary


class CeleryTaskTest(TestCase):
    @patch('analysis.management.commands.make_day_summary.Command.handle')
    def test_make_day_summary_task(self, mock_handle):
        result = make_day_summary.delay()
        self.assertTrue(result.successful())
        mock_handle.assert_called_once()

    @patch('analysis.management.commands.make_week_summary.Command.handle')
    def test_make_week_summary_task(self, mock_handle):
        result = make_week_summary.delay()
        self.assertTrue(result.successful())
        mock_handle.assert_called_once()

