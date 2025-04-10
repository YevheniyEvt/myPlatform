from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from ..models import Note
from . import test_utils

class NoteListViewTestCase(TestCase):
    """Test list of Notes"""

    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_note_data()
        cls.note_1 = Note.objects.get(text='note_1_text_1')
        cls.note_2_1 = Note.objects.get(text='note_2_text_1')
        cls.note_2 = Note.objects.get(text='note_1_text_2')
        cls.user_1 = User.objects.get(username='user_name_1')
        cls.notes_queryset = Note.objects.filter(user=cls.user_1).order_by('-date')

    def test_get_notes_not_login_user(self):
        response = self.client.get(reverse('notebook:notes_list_view'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/notes-list/', target_status_code=200)
        
    def test_get_notes_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:notes_list_view'))
        self.assertQuerySetEqual(response.context['notes'], self.notes_queryset[:5])
        self.assertTemplateUsed(response, 'notebook/note_list.html')

    def test_get_notes_user_is_not_owner(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.get(reverse('notebook:notes_list_view'))
        self.assertNotContains(response, self.note_1.text, status_code=200)
        self.assertNotContains(response, self.note_2_1.text, status_code=200)
        
    def test_get_notes_with_search(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:notes_list_view'), query_params={'search': 'note_2'})
        self.assertContains(response, self.note_2_1.text, status_code=200, count=1)
        self.assertNotContains(response, self.note_1.text, status_code=200)
        self.assertNotContains(response, self.note_2.text, status_code=200)
        self.assertQuerySetEqual(response.context['notes'], [self.note_2_1])
        self.assertTemplateUsed(response, 'notebook/note_list.html')
#
    def test_get_notes_with_search_not_exist(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:notes_list_view'), query_params={'search': ''.join('abc' for _ in range(4))})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['notes'], [])
     
    def test_get_paginate_notes_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:notes_list_view'), query_params={'page': '2'})
        for note in self.notes_queryset[:5]:
            with self.subTest(note=note):
                self.assertNotContains(response, note.text, status_code=200)
        self.assertEqual(len(response.context['notes']), 5)
        self.assertTemplateUsed(response, 'notebook/note_list.html')

class NoteCreateViewTestCase(TestCase):
    """Test create note"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_users_data()
    
    def test_create_note_not_login_user(self):
        response = self.client.post(
            reverse('notebook:notes_list_view'),
            data={"text": "created_text"},
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/notes-list/', target_status_code=200)

    def test_create_note(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(
            reverse('notebook:notes_list_view'),
            data={"text": "created_text"},
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:notes_list_view'), target_status_code=200)
        self.assertIsNotNone(Note.objects.filter(text='created_text').first())


class NoteUpdateViewTestCase(TestCase):
    """Test update note"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_note_data()
        cls.user_1 = User.objects.get(username='user_name_1')
        cls.note_1 = Note.objects.get(text='note_1_text_1')
        cls.notes_queryset = Note.objects.filter(user=cls.user_1)

    def test_update_note_not_login_user(self):
        response = self.client.post(reverse('notebook:notes_update_view',
                                            kwargs={"pk": self.note_1.id}),
                                            data={"text": "updated_text"},
                                            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login')}?next=/notebook/notes-list/update/{self.note_1.id}/', target_status_code=200)
    
    def test_update_note_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:notes_update_view',
                                            kwargs={"pk": self.note_1.id}),
                                            data={"text": "updated_text"},
                                            )
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Note.objects.filter(text='note_1_text_1').first())
        self.assertIsNone(Note.objects.filter(text='updated_text').first())

    def test_update_note_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:notes_update_view',
                                            kwargs={"pk": self.note_1.id}),
                                            data={"text": "updated_text"},
                                            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:notes_list_view'), target_status_code=200)
        self.assertIsNotNone(Note.objects.filter(text='updated_text').first())
        self.assertIsNone(Note.objects.filter(text='note_1_text_1').first())

    def test_update_note_get(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:notes_update_view',
                                            kwargs={"pk": self.note_1.id}),
                                            )
        self.assertQuerySetEqual(response.context['notes'], self.notes_queryset[:5])
        self.assertEqual(response.context['update_note'], self.note_1)

    
class NotesDeleteTestCase(TestCase):
    """Test delete note"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_note_data()
        cls.note_1 = Note.objects.get(text='note_1_text_1')

    def test_delete_note_not_login_user(self):
        response = self.client.post(reverse('notebook:notes_delete_view',kwargs={"pk": self.note_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('user:login', )}?next=/notebook/notes-list/delete/{self.note_1.id}/', target_status_code=200)
    
    def test_delete_note_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:notes_delete_view',kwargs={"pk": self.note_1.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Note.objects.filter(text='note_1_text_1').first())

    def test_delete_note_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:notes_delete_view',kwargs={"pk": self.note_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:notes_list_view'), target_status_code=200)
        self.assertIsNone(Note.objects.filter(text='note_1_text_1').first())
