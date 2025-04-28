from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from tasks.models import Task
from comunication.models import Coment


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

