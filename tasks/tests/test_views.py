from datetime import timedelta
import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from projects.models import Project
from tasks.models import Task, TaskChangeLog, TaskResult
from tasks.tasks import apply_overdue_penalties
from users.models import User, Company


class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Acme")
        self.creator = User.objects.create_user(username='creator', password='pass', company=self.company)
        self.assignee = User.objects.create_user(username='assignee', password='pass', company=self.company)
        self.project = Project.objects.create(name='Test Project', company=self.company, created_by=self.creator)
        self.project.participants.add(self.creator, self.assignee)

    def test_add_task(self):
        self.client.login(username='creator', password='pass')
        response = self.client.post(reverse('tasks:add_task', kwargs={"id": self.project.id}), {
            'name': 'Task title',
            'description': 'Task description',
            'assignee': self.assignee.id,
            'priority': 'MEDIUM',
            'deadline': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
        })

        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Task title')
        self.assertEqual(task.assignee, self.assignee)
        self.assertEqual(task.creator, self.creator)
        self.assertEqual(task.status, Task.Status.NEW)

    def test_status_workflow_and_permissions(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator,
                                   assignee=self.assignee, deadline=timezone.now() + timedelta(days=1))
        url = reverse('tasks:task_change_status', kwargs={"id": self.project.id})

        self.client.login(username='creator', password='pass')
        response = self.client.post(url, {'task_id': task.id, 'new_status': 'IN_PROGRESS'})
        self.assertTrue(response.json()['success'])
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)

        response = self.client.post(url, {'task_id': task.id, 'new_status': 'ON_REVIEW'})
        self.assertTrue(response.json()['success'])
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.ON_REVIEW)

        response = self.client.post(url, {'task_id': task.id, 'new_status': 'DONE'})
        self.assertTrue(response.json()['success'])
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)
        self.assertIsNotNone(task.completed_at)

    def test_kanban_move_updates_status_and_position(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator,
                                   assignee=self.assignee, position=1)
        url = reverse('tasks:kanban_move', kwargs={"id": self.project.id})
        self.client.login(username='assignee', password='pass')
        payload = {
            "task_id": task.id,
            "new_status": "IN_PROGRESS",
            "target_order": [task.id],
            "source_order": [task.id],
        }
        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)
        self.assertEqual(task.position, 1)
        self.assertTrue(TaskChangeLog.objects.filter(task=task, field_name="status").exists())

    def test_kanban_move_allows_any_transition(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator,
                                   assignee=self.assignee, position=1)
        url = reverse('tasks:kanban_move', kwargs={"id": self.project.id})
        self.client.login(username='assignee', password='pass')
        payload = {
            "task_id": task.id,
            "new_status": "DONE",
            "target_order": [task.id],
        }
        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)

    def test_kanban_reorder_within_column(self):
        task1 = Task.objects.create(name='Task1', project=self.project, creator=self.creator,
                                    assignee=self.assignee, position=1)
        task2 = Task.objects.create(name='Task2', project=self.project, creator=self.creator,
                                    assignee=self.assignee, position=2)
        url = reverse('tasks:kanban_move', kwargs={"id": self.project.id})
        self.client.login(username='creator', password='pass')
        payload = {
            "task_id": task2.id,
            "new_status": "NEW",
            "target_order": [task2.id, task1.id],
        }
        response = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        task1.refresh_from_db()
        task2.refresh_from_db()
        self.assertEqual(task2.position, 1)
        self.assertEqual(task1.position, 2)

    def test_update_task_logs_changes(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator, assignee=self.assignee)
        self.client.login(username='creator', password='pass')
        response = self.client.post(reverse('tasks:task_update_info', kwargs={"id": self.project.id}), {
            'task_id': task.id,
            'name': 'Task updated',
            'description': 'New description',
            'assignee': self.assignee.id,
            'priority': 'HIGH',
            'deadline': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M'),
        })
        self.assertEqual(response.status_code, 200)
        self.assertGreater(TaskChangeLog.objects.filter(task=task).count(), 0)

    def test_add_result(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator, assignee=self.assignee)
        self.client.login(username='assignee', password='pass')
        response = self.client.post(reverse('tasks:add_result', kwargs={"id": self.project.id}), {
            'task_id': task.id,
            'message': 'Result message',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TaskResult.objects.filter(task=task).count(), 1)

    def test_kanban_list_filters(self):
        Task.objects.create(name='Task A', project=self.project, creator=self.creator,
                            assignee=self.assignee, status=Task.Status.NEW)
        Task.objects.create(name='Task B', project=self.project, creator=self.creator,
                            assignee=self.creator, status=Task.Status.NEW)
        self.client.login(username='creator', password='pass')
        url = reverse('tasks:kanban_list', kwargs={"id": self.project.id})
        response = self.client.get(url, {'column_status': 'NEW', 'assignee': self.assignee.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['total'], 1)

    def test_bonus_on_time_completion(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator,
                                   assignee=self.assignee, deadline=timezone.now() + timedelta(days=1))
        self.client.login(username='assignee', password='pass')
        self.client.post(reverse('tasks:task_change_status', kwargs={"id": self.project.id}),
                         {'task_id': task.id, 'new_status': 'IN_PROGRESS'})
        self.client.post(reverse('tasks:task_change_status', kwargs={"id": self.project.id}),
                         {'task_id': task.id, 'new_status': 'ON_REVIEW'})
        self.client.login(username='creator', password='pass')
        self.client.post(reverse('tasks:task_change_status', kwargs={"id": self.project.id}),
                         {'task_id': task.id, 'new_status': 'DONE'})
        self.assignee.refresh_from_db()
        self.assertGreater(self.assignee.bonus_balance, 0)

    def test_overdue_penalty_applied_once(self):
        task = Task.objects.create(name='Task', project=self.project, creator=self.creator,
                                   assignee=self.assignee, deadline=timezone.now() - timedelta(days=1))
        apply_overdue_penalties()
        task.refresh_from_db()
        self.assertTrue(task.overdue_penalty_applied)
        self.assignee.refresh_from_db()
        first_balance = self.assignee.bonus_balance
        apply_overdue_penalties()
        self.assignee.refresh_from_db()
        self.assertEqual(self.assignee.bonus_balance, first_balance)
