from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from employee.models import Store
from tasks.models import Task, TaskHistory, TaskUsers


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


class TaskUpdateViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = Task.objects.filter(taskusers__user=self.user).distinct().first()

    def test_update_task_not_login_user(self):
        response = self.client.post(reverse('tasks:update_task', kwargs={'pk': self.my_task.id}),
                                    data={'content': 'hello test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/update/{self.my_task.id}/',
                            target_status_code=200,
                            )
        
    def test_update_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:update_task', kwargs={'pk': self.my_task.id}),
                                    data={
                                        'title': 'hello test',
                                        'content': 'hello test',
                                        'start_date': '2025-04-07',
                                        'deadline': '2025-04-07',
                                        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            reverse('tasks:detail_task', kwargs={'pk': self.my_task.id}),
                            target_status_code=200,
                            )
        task = Task.objects.get(id=self.my_task.id)
        self.assertEqual(task.title, 'hello test')

    def test_update_not_allowed_task(self):
        task = Task.objects.exclude(taskusers__user=self.user).first()
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:update_task', kwargs={'pk': task.id}),
                                    data={
                                        'title': 'hello test',
                                        'content': 'hello test',
                                        'start_date': '2025-04-07',
                                        'deadline': '2025-04-07',
                                        })
        self.assertEqual(response.status_code, 404)
        task = Task.objects.get(id=task.id)
        self.assertNotEqual(task.title, 'hello test')


class TaskDeleteViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = TaskUsers.objects.filter(user=self.user).first()

    def test_delete_task_not_login_user(self):
        response = self.client.post(reverse('tasks:delete_task', kwargs={'pk': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/delete/{self.my_task.id}/',
                            target_status_code=200,
                            )
        
    def test_delete_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:delete_task', kwargs={'pk': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:my_tasks'),target_status_code=200)
        task = TaskUsers.objects.filter(id=self.my_task.id).first()
        self.assertIsNone(task)

    def test_delete_not_allowed_task(self):
        task = TaskUsers.objects.exclude(Q(user=self.user) | Q(creator=True)).first()
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:delete_task', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 404)
        task_not_deleted = TaskUsers.objects.filter(id=task.id).first()
        self.assertIsNotNone(task_not_deleted)


class CompleteTaskTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = TaskUsers.objects.filter(user=self.user, completed=False, not_accepted=False).first()

    def test_complete_task_not_login_user(self):
        response = self.client.post(reverse('tasks:complete_task', kwargs={'task_id': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/complete/{self.my_task.id}/',
                            target_status_code=200,
                            )
    
    def test_compete_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:complete_task', kwargs={'task_id': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:my_active_task'), target_status_code=200)
        task = TaskUsers.objects.get(id=self.my_task.id)
        self.assertTrue(task.completed)
        self.assertFalse(task.not_accepted)
        task_history = TaskHistory.objects.filter(task=task, user=self.user, complete=True).first()
        self.assertIsNotNone(task_history)


class OpenCompletedTaskTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = TaskUsers.objects.filter(user=self.user, completed=True).first()

    def test_open_task_not_login_user(self):
        response = self.client.post(reverse('tasks:open_task', kwargs={'task_id': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/open/{self.my_task.id}/',
                            target_status_code=200,
                            )
    
    def test_open_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:open_task', kwargs={'task_id': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:my_completed_task'), target_status_code=200)
        task = TaskUsers.objects.get(id=self.my_task.id)
        self.assertFalse(task.completed)
        self.assertFalse(task.not_accepted)
        task_history = TaskHistory.objects.filter(task=task, user=self.user, reopen=True).first()
        self.assertIsNotNone(task_history)


class NotAcceptedTaskTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = TaskUsers.objects.filter(user=self.user, completed=False, not_accepted=False).first()

    def test_open_task_not_login_user(self):
        response = self.client.post(reverse('tasks:not_accept_task', kwargs={'task_id': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/not-accept/{self.my_task.id}/',
                            target_status_code=200,
                            )
    
    def test_open_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:not_accept_task', kwargs={'task_id': self.my_task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:my_active_task'), target_status_code=200)
        task = TaskUsers.objects.get(id=self.my_task.id)
        self.assertFalse(task.completed)
        self.assertTrue(task.not_accepted)