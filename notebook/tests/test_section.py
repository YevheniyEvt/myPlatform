from django.test import TestCase
from django.urls import reverse

from ..models import Topic, Section
from .test_utils import create_test_topic_data, create_test_section_data

class TopicDetailSectionListTestCase(TestCase):
    """Test Topic detail, it is a Section list(section_set)"""
    @classmethod
    def setUpTestData(cls):
        create_test_section_data()
        cls.topic_1 = Topic.objects.get(name='topic_name_1')
        cls.section_1 = Section.objects.get(title='title_section_number_1')
        cls.section_2 = Section.objects.get(title='title_section_number_2')
        cls.topic_1_sections_queryset = Section.objects.filter(topic=cls.topic_1).order_by('id')

    def test_get_topic_not_login_user(self):
        response = self.client.get(reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/{self.topic_1.id}/', target_status_code=200)

    def test_get_topic_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}))
        self.assertContains(response, self.topic_1.short_description, status_code=200, count=1)
        self.assertContains(response, self.topic_1.name, status_code=200, count=1)
        self.assertQuerySetEqual(response.context['sections'].order_by('id'), self.topic_1_sections_queryset)
        self.assertEqual(response.context['topic_object'], self.topic_1)
        self.assertTemplateUsed(response, 'notebook/topic_detail.html')

    def test_get_sections_user_not_owner(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.get(reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}))

        for section in self.topic_1_sections_queryset:
            with self.subTest(section=section):
                self.assertContains(response, section.title, status_code=200, count=1)
                self.assertContains(response, section.description, status_code=200, count=1)

    def test_get_sections_with_search(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(
            reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}),
            query_params={'search': 'section_number_1'}
            )
        self.assertContains(response, self.section_1.title, status_code=200, count=1)
        self.assertContains(response, self.section_1.description, status_code=200, count=1)
        self.assertNotContains(response, self.section_2.title, status_code=200)
        self.assertNotContains(response, self.section_2.description, status_code=200)
        self.assertQuerySetEqual(response.context['sections'], [self.section_1])
        self.assertTemplateUsed(response, 'notebook/topic_detail.html')

    def test_get_sections_with_search_not_exist(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(
            reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}),
            query_params={'search': ''.join('abc' for _ in range(4))})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['sections'], [])
        

class CreateSectionTestCase(TestCase):
    """Test create Section"""
    @classmethod
    def setUpTestData(cls):
        create_test_topic_data()
        cls.topic_1 = Topic.objects.get(name='topic_name_1')

    def test_create_section_not_login_user(self):
        response = self.client.post(reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}),
                                   data={"title": "created_name", "description": "created_description"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/{self.topic_1.id}/', target_status_code=200)

    def test_create_section(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}),
                                   data={"title": "created_name", "description": "created_description"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:topic_detail', kwargs={"pk": self.topic_1.id}), target_status_code=200)
        self.assertIsNotNone(Section.objects.filter(title='created_name').first())

class SectionDeleteViewTestCase(TestCase):
    """Test delete Section"""
    @classmethod
    def setUpTestData(cls):
        create_test_section_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_delete_section_not_login_user(self):
        response = self.client.post(reverse('notebook:delete_section',kwargs={"pk": self.section_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/delete-section/{self.section_1.id}/', target_status_code=200)
    
    def test_delete_section_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:delete_section',kwargs={"pk": self.section_1.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Section.objects.filter(title='title_section_number_1').first())

    def test_delete_section_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:delete_section',kwargs={"pk": self.section_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:topic_detail', kwargs={"pk": self.section_1.topic.id}), target_status_code=200)
        self.assertIsNone(Section.objects.filter(title='title_section_number_1').first())
