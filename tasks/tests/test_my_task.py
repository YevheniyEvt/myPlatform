from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from tasks.models import Task, TaskHistory
from tasks.utils import get_users_from_location
from employee.utils import get_user_location

from comunication.models import Coment


class MyTasksLIstViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')

    def test_get_task_not_login_user(self):
        response = self.client.get(reverse('tasks:my_tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/all/',
                            target_status_code=200,
                            )
        
    def test_get_all_my_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:my_tasks'))
        my_task = Task.objects.filter(taskusers__user=self.user)

        self.assertQuerySetEqual(response.context['tasks'], my_task, ordered=False)
        self.assertEqual(response.status_code, 200)
        attributes = ['revised', 'completed', 'not_accepted', 'is_creator', 'task_user_id']
        for attr in attributes:
                with self.subTest(attr=attr):
                    self.assertTrue(hasattr(response.context['tasks'][0], attr))

    def test_get_all_my_active_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:my_active_task'))
        my_task = (Task.objects.
                    filter(taskusers__user=self.user).
                    exclude(
                      Q(taskusers__completed=True) | 
                      Q(taskusers__not_accepted=True)
                      ))

        self.assertQuerySetEqual(response.context['tasks'], my_task, ordered=False)
        self.assertEqual(response.status_code, 200)

    def test_get_all_my_completed_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:my_completed_task'))
        my_task = (Task.objects.
                    filter(taskusers__user=self.user).
                    filter(
                      Q(taskusers__completed=True) |
                      Q(taskusers__not_accepted=True)
                      ))

        self.assertQuerySetEqual(response.context['tasks'], my_task, ordered=False)
        self.assertEqual(response.status_code, 200)


class TaskDetailViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = Task.objects.filter(taskusers__user=self.user).first()

    def test_get_task_not_login_user(self):
        response = self.client.get(reverse('tasks:detail_task', kwargs={'pk': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/{self.my_task.id}/',
                            target_status_code=200,
                            )

    def test_get_detail_my_task(self):
        self.client.force_login(self.user)
        task_user = self.my_task.taskusers_set.filter(user=self.user).first()
        response = self.client.get(reverse('tasks:detail_task', kwargs={'pk': self.my_task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task_user'], task_user)
        task_user_after_get = self.my_task.taskusers_set.filter(user=self.user).first()
        self.assertIsNotNone(task_user_after_get.revised)

        task_history = TaskHistory.objects.filter(user=self.user, task=task_user).first()
        self.assertIsNotNone(task_history)
        self.assertTrue(task_history.revised)

        comments = Coment.objects.filter(task=task_user.task)
        self.assertQuerySetEqual(response.context['comments'], comments)

        task_history_context = TaskHistory.objects.filter(task=task_user)
        self.assertQuerySetEqual(response.context['task_history'], task_history_context)

    def test_get_detail_task_from_my_location(self):
        current_user_location = get_user_location(self.user)
        my_location_users = get_users_from_location(recipients_id=[current_user_location.id],
                                                        recipients=current_user_location
                                                        )
        task_from_my_location = Task.objects.filter(taskusers__user__in=my_location_users).distinct().first()
        task_user = task_from_my_location.taskusers_set.first()

        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:detail_task',
                                           kwargs={'pk': task_from_my_location.id,
                                                   'user_id': task_user.user.id,
                                                   }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task_user'], task_user)
        self.assertIsNone(task_user.revised)

        task_history_fake = TaskHistory.objects.filter(user=task_user.user, task=task_user).first()
        self.assertIsNone(task_history_fake)

        task_history = TaskHistory.objects.filter(user=self.user, task=task_user).first()
        self.assertIsNotNone(task_history)
        self.assertTrue(task_history.revised)

        self.assertFalse(hasattr(response.context, 'comments'))

    def test_get_not_allowed_task(self):
        task = Task.objects.exclude(taskusers__user=self.user).first()
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:detail_task',
                                           kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 404)

