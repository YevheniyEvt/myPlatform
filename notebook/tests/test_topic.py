from django.test import TestCase
from django.urls import reverse

from ..models import Topic
from .test_utils import create_test_users_data, create_test_topic_data

class TopicListViewTestCase(TestCase):
    """Test list of topic"""
    @classmethod
    def setUpTestData(cls):
        create_test_topic_data()
        cls.topic_1 = Topic.objects.get(name='topic_name_1')
        cls.topic_2 = Topic.objects.get(name='topic_name_2')
        cls.topics_queryset = Topic.objects.all().order_by('id')

    def test_get_topics_not_login_user(self):
        response = self.client.get(reverse('notebook:topic_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/', target_status_code=200)
        
    def test_get_topics_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:topic_list'))
        self.assertContains(response, self.topic_1.short_description, status_code=200, count=1)
        self.assertContains(response, self.topic_1.name, status_code=200, count=1)
        self.assertQuerySetEqual(response.context['topics'].order_by('id'), self.topics_queryset)
        self.assertTemplateUsed(response, 'notebook/topic_list.html')

    def test_get_topics_user_is_not_owner(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.get(reverse('notebook:topic_list'))
        self.assertContains(response, self.topic_1.short_description, status_code=200, count=1)
        self.assertContains(response, self.topic_1.name, status_code=200, count=1)
        self.assertQuerySetEqual(response.context['topics'].order_by('id'), self.topics_queryset)

    def test_get_topics_with_search(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:topic_list'), query_params={'search': 'short_description1'})
        self.assertContains(response, self.topic_1.short_description, status_code=200, count=1)
        self.assertContains(response, self.topic_1.name, status_code=200, count=1)
        self.assertNotContains(response, self.topic_2.short_description, status_code=200)
        self.assertNotContains(response, self.topic_2.name, status_code=200)
        self.assertQuerySetEqual(response.context['topics'], [self.topic_1])
        self.assertTemplateUsed(response, 'notebook/topic_list.html')

    def test_get_topics_with_search_not_exist(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:topic_list'), query_params={'search': ''.join('abc' for _ in range(4))})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['topics'], [])
    
class TopicCreateViewTestCase(TestCase):
    """Test create topic"""
    @classmethod
    def setUpTestData(cls):
        create_test_users_data()
    
    def test_create_topic_not_login_user(self):
        response = self.client.post(
            reverse('notebook:create_topic'),
            data={"name": "created_name", "short_description": "created_short_description"},
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/create-topic/', target_status_code=200)

    def test_create_topic(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(
            reverse('notebook:create_topic'),
            data={"name": "created_name", "short_description": "created_short_description"},
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:topic_list'), target_status_code=200)
        self.assertIsNotNone(Topic.objects.filter(name='created_name').first())
    
    def user_without_perm_get_create_topic(self):
        response = self.client.get(reverse('notebook:create_topic'))
        self.assertEqual(response.status_code, 404)

class TopicDeleteViewTestCase(TestCase):
    """Test delete topic"""
    @classmethod
    def setUpTestData(cls):
        create_test_topic_data()
        cls.topic_1 = Topic.objects.get(name='topic_name_1')

    def test_delete_topic_not_login_user(self):
        response = self.client.post(reverse('notebook:delete_topic',kwargs={"pk": self.topic_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/delete-topic/{self.topic_1.id}/', target_status_code=200)
    
    def test_delete_topic_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:delete_topic',kwargs={"pk": self.topic_1.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Topic.objects.filter(name='topic_name_1').first())

    def test_delete_topic_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:delete_topic',kwargs={"pk": self.topic_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:topic_list'), target_status_code=200)
        self.assertIsNone(Topic.objects.filter(name='topic_name_1').first())
