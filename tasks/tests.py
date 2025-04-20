from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from employee.models import Store
from tasks.models import Task, TaskHistory
from tasks.utils import employee_tasks_allowed_locations

# Create your tests here.


class CreateTaskViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.filter(storeemployee__isnull=False).first()
        return super().setUp()

    def test_create_task_user_not_login(self):
        response=self.client.post(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/create/',
                            target_status_code=200,
                            )

    def test_create_quick_task_user_login(self):
        self.client.force_login(self.user)
        response=self.client.post(reverse('tasks:create_task'),
                                  data={
                                    'title': 'Hello test',
                                    'content': 'Hello test',
                                    'deadline': '2025-04-07',
                                    'start_date': '2025-04-07',
                                    'recipients': [self.user.id]
                                  })
        self.assertIsNotNone(Task.objects.filter(title='Hello test').first())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:create_task'), target_status_code=200)
        self.assertIsNotNone(Task.objects.filter(title='Hello test').first())
        self.assertIsNotNone(Task.objects.
                             filter(title='Hello test').
                             first().taskusers_set.
                             filter(user=self.user)
                             )
        self.assertEqual(Task.objects.
                             filter(title='Hello test').
                             first().taskusers_set.
                             filter(creator=True).first().user, self.user
                             )
        
    def test_create_distribution_task_storeemployee(self):
        store = self.user.storeemployee.store
        recipients = User.objects.filter(storeemployee__store=store)
        self.client.force_login(self.user)
        response=self.client.post(reverse('tasks:create_task'),
                                  data={
                                    'title': 'Hello test',
                                    'content': 'Hello test',
                                    'deadline': '2025-04-07',
                                    'start_date': '2025-04-07',
                                    'recipients': [user.id for user in recipients]
                                  })
        self.assertIsNotNone(Task.objects.filter(title='Hello test').first())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:create_task'), target_status_code=200)
        self.assertIsNotNone(Task.objects.filter(title='Hello test').first())
        self.assertIsNotNone(Task.objects.
                             filter(title='Hello test').
                             first().taskusers_set.
                             filter(user=recipients[0])
                             )
        self.assertEqual(Task.objects.
                             filter(title='Hello test').
                             first().taskusers_set.
                             filter(creator=True).first().user, self.user
                             )

    def test_create_distribution_task_retail(self):
        user = User.objects.filter(retailemployee__isnull=False).filter(retailemployee__district__isnull=False).first()
        district = user.retailemployee.district
        recipients = Store.objects.filter(district=district)
        self.client.force_login(user)
        response=self.client.post(reverse('tasks:create_task'),
                                  data={
                                    'title': 'Hello test',
                                    'content': 'Hello test',
                                    'deadline': '2025-04-07',
                                    'start_date': '2025-04-07',
                                    'recipients': [store.id for store in recipients]
                                  })
        self.assertIsNotNone(Task.objects.filter(title='Hello test').first())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:create_task'), target_status_code=200)
        self.assertIsNotNone(Task.objects.filter(title='Hello test').first())
        self.assertIsNotNone(Task.objects.
                             filter(title='Hello test').
                             first().taskusers_set.
                             filter(user=user)
                             )
        self.assertEqual(Task.objects.
                             filter(title='Hello test').
                             first().taskusers_set.
                             filter(creator=True).first().user, user
                             )



class MyTasksLIstViewTestCase(TestCase):
    fixtures = ["test_data"]
    pass
    