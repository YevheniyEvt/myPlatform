from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models import Q

from employee.models import Store
from tasks.models import Task, TaskHistory, TaskUsers
from tasks.utils import employee_tasks_allowed_locations, users_to_tasks_create, get_users_from_location
from employee.utils import get_user_location, get_management_positions

from comunication.models import Coment, DeleteHistory



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


class CreateTaskCommentViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = Task.objects.filter(taskusers__user=self.user).distinct().first()
    
    def test_create_comment_not_login_user(self):
        response = self.client.post(reverse('tasks:detail_task', kwargs={'pk': self.my_task.id}),
                                    data={'content': 'hello test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/{self.my_task.id}/',
                            target_status_code=200,
                            )

    def test_create_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:detail_task', kwargs={'pk': self.my_task.id}),
                                    data={'content': 'hello test'})
        self.assertEqual(response.status_code, 302)
        comment = Coment.objects.filter(content='hello test').first()
        self.assertIsNotNone(comment)

    def test_create_comment_not_allowed_task(self):
        task = Task.objects.exclude(taskusers__user=self.user).distinct().first()
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:detail_task', kwargs={'pk': task.id}),
                                    data={'content': 'hello test'})
        self.assertEqual(response.status_code, 404)


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

class CommentDeleteViewTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        my_task = Task.objects.filter(taskusers__user=self.user).distinct().first()
        Coment.objects.create(
            task=my_task,
            owner=self.user,
            content='hello test'
        )
        self.comment = Coment.objects.get(content='hello test')

    def test_del_comment_to_login_user(self):
        response = self.client.post(reverse('tasks:delete_coment', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/tasks/delete/coment/{self.comment.id}/',
                            target_status_code=200,
                            )
        
    def test_delete_comment(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:delete_coment', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:detail_task', kwargs={'pk': self.comment.task.id}),target_status_code=200)
        comment = Coment.objects.filter(id=self.comment.id).first()
        self.assertIsNone(comment)

    def test_delete_not_user_comment(self):
        user = User.objects.exclude(username='admin').first()
        self.client.force_login(user)
        response = self.client.post(reverse('tasks:delete_task', kwargs={'pk': self.comment.id}))
        self.assertEqual(response.status_code, 404)
        comment = Coment.objects.filter(id=self.comment.id).first()
        self.assertIsNotNone(comment)


class CompleteTaskTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.my_task = TaskUsers.objects.filter(user=self.user, completed=False).first()

    