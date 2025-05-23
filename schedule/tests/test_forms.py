from datetime import datetime, timedelta

from django.test import TestCase

from schedule.forms import TaskCreateForm, TaskCommentForm



class TaskCreateFormTestCase(TestCase):
    def test_create_task(self):
        form_data = {'name': 'Title for the test task',
                     'description': 'Description for the test task',
                     'start_date': datetime.now().date(),
                     'start_time': datetime.now().time(),
                     'due_date': datetime.now().date() + timedelta(days=1),
                     'due_time': datetime.now().time()}
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_task_with_invalid_due_date(self):
        form_data = {'name': 'Title for the test task',
                     'description': 'Description for the test task',
                     'start_date': datetime.now().date(),
                     'start_time': datetime.now().time(),
                     'due_date': datetime.now().date() - timedelta(days=1),
                     'due_time': datetime.now().time()}
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_task_with_invalid_start_date(self):
        form_data = {'name': 'Title for the test task',
                     'description': 'Description for the test task',
                     'start_date': datetime.now().date() - timedelta(days=1),
                     'start_time': datetime.now().time(),
                     'due_date': datetime.now().date(),
                     'due_time': datetime.now().time()}
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_task_with_invalid_name(self):
        form_data = {'name': '#########',
                     'description': 'Description for the test task',
                     'start_date': datetime.now().date(),
                     'start_time': datetime.now().time(),
                     'due_date': datetime.now().date() + timedelta(days=1),
                     'due_time': datetime.now().time()}

        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_task_with_invalid_description(self):
        form_data = {'name': 'Title for the test task',
                     'description': '#########',
                     'start_date': datetime.now().date(),
                     'start_time': datetime.now().time(),
                     'due_date': datetime.now().date() + timedelta(days=1),
                     'due_time': datetime.now().time()}

        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class CommentFormTestCase(TestCase):
    def test_create_comment(self):
        form_data = {'text': 'Comment for the test task'}
        form = TaskCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_comment_with_invalid_text(self):
        form_data = {'text': '#########'}
        form = TaskCommentForm(data=form_data)
        self.assertFalse(form.is_valid())
