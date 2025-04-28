from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from tasks.utils import get_users_from_location
from employee.utils import get_user_location
from tasks.models import Task

class MyLocationTaskViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        current_user_location = get_user_location(self.user)
        self.my_location_users = get_users_from_location(recipients_id=[current_user_location.id],
                                                        recipients=current_user_location
                                                        )
    def test_get_location_tasks_not_login_user(self):
        response = self.client.get(reverse('tasks:my_location_tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/location/',
                            target_status_code=200,
                            )
      
    def test_get_location_tasks(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('tasks:my_location_tasks'))
        tasks = Task.objects.filter(taskusers__user__in=self.my_location_users).distinct()
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['tasks'], tasks, ordered=False)


class LocationTaskDetailViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        current_user_location = get_user_location(self.user)
        self.my_location_users = get_users_from_location(recipients_id=[current_user_location.id],
                                                        recipients=current_user_location
                                                        )
        self.task = Task.objects.filter(taskusers__user__in=self.my_location_users).first()
        
    def test_get_task_not_login_user(self):
        response = self.client.get(reverse('tasks:detail_location_task', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/location/{self.task.id}/',
                            target_status_code=200,
                            )
        
    def test_get_my_location_task(self):
        self.client.force_login(self.user)
        tasks_users = self.task.taskusers_set.filter(user__in=self.my_location_users)
        response = self.client.get(reverse('tasks:detail_location_task', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['tasks_users'], tasks_users, ordered=False)
        self.assertEqual(response.context['task'], self.task)

    def test_get_not_my_location_task(self):
        user2 = User.objects.all()[1]
        current_user_location = get_user_location(user2)
        my_location_users = get_users_from_location(recipients_id=[current_user_location.id],
                                                        recipients=current_user_location
                                                        )
        task = Task.objects.exclude(taskusers__user__in=my_location_users).exclude(taskusers__user=user2).first()
        self.client.force_login(user2)
        response = self.client.get(reverse('tasks:detail_location_task', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 404)



