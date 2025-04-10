from django.test import TestCase
from django.urls import reverse


from ..models import Section, Code, Links, Article, Image
from . import test_utils


class CodeSectionDetailViewTestCase(TestCase):
    """Test detail of section with code"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_code_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')
        cls.code_1_query = Code.objects.get(content=f'code_content_number1')
        cls.code_2_query = Code.objects.get(content=f'code_content_number2')
        cls.codes_queryset = Code.objects.filter(section=cls.section_1).order_by('id')

    def test_get_codes_not_login_user(self):
        response = self.client.get(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/detail-section/{self.section_1.id}/code/',
                            target_status_code=200
                            )
        
    def test_get_codes_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}))
        self.assertContains(response, self.section_1.title, status_code=200, count=1)
        self.assertContains(response, self.section_1.description, status_code=200, count=1)
        self.assertQuerySetEqual(response.context['code_queryset'].order_by('id'), self.codes_queryset)
        self.assertEqual(response.context['section_object'], self.section_1)
        self.assertTemplateUsed(response, 'notebook/section_detail.html')
        self.assertTemplateUsed(response, 'notebook/code_list.html')

    def test_get_codes_user_not_owner(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.get(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}))

        for code in self.codes_queryset:
            with self.subTest(code=code):
                self.assertContains(response, code.content, status_code=200, count=1)


    def test_get_codes_with_search(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}),
                                   query_params={'search': 'content_number1'},
                                   )
   
        self.assertContains(response, self.code_1_query.content, status_code=200, count=1)
        self.assertNotContains(response, self.code_2_query.content, status_code=200)
        self.assertQuerySetEqual(response.context['code_queryset'], [self.code_1_query])
        self.assertTemplateUsed(response, 'notebook/section_detail.html')

    def test_get_codes_with_search_not_exist(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}),
                                   query_params={'search': ''.join('abc' for _ in range(4))},
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['code_queryset'], [])

class CreateCodeSectionView(TestCase):
    """Test create Code"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_section_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_create_code_not_login_user(self):
        response = self.client.post(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}),
                                   data={"title": "created_name"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/detail-section/{self.section_1.id}/code/',
                            target_status_code=200
                            )

    def test_create_code(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}),
                                   data={"content": "created_name"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}), target_status_code=200)
        self.assertIsNotNone(Code.objects.filter(content='created_name').first())

class CodeSectionDeleteViewTestCase(TestCase):
    """Test delete Code"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_code_data()
        cls.code_1_query = Code.objects.get(content=f'code_content_number1')
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_delete_code_not_login_user(self):
        response = self.client.post(reverse('notebook:code_delete',kwargs={"pk": self.code_1_query.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/delete-code/{self.code_1_query.id}/',
                            target_status_code=200
                            )
    
    def test_delete_code_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:code_delete',kwargs={"pk": self.code_1_query.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Code.objects.filter(content='code_content_number1').first())

    def test_delete_code_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:code_delete',kwargs={"pk": self.code_1_query.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:show_cod', kwargs={"pk": self.section_1.id}), target_status_code=200)
        self.assertIsNone(Code.objects.filter(content='code_content_number1').first())


class ArticleSectionViewTestCase(TestCase):
    """Test detail of section with article"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_article_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')
        cls.article_1_query = Article.objects.get(content='article_content_number1')
        cls.article_2_query = Article.objects.get(content='article_content_number2')
        cls.articles_queryset = Article.objects.filter(section=cls.section_1).order_by('id')

    def test_get_articles_not_login_user(self):
        response = self.client.get(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/detail-section/{self.section_1.id}/article/',
                            target_status_code=200
                            )
        
    def test_get_articles_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}))
        self.assertContains(response, self.section_1.title, status_code=200, count=1)
        self.assertContains(response, self.section_1.description, status_code=200, count=1)
        self.assertQuerySetEqual(response.context['article_queryset'].order_by('id'), self.articles_queryset)
        self.assertEqual(response.context['section_object'], self.section_1)
        self.assertTemplateUsed(response, 'notebook/section_detail.html')
        self.assertTemplateUsed(response, 'notebook/article_list.html')

    def test_get_articles_user_not_owner(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.get(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}))

        for article in self.articles_queryset:
            with self.subTest(article=article):
                self.assertContains(response, article.content, status_code=200, count=1)


    def test_get_articles_with_search(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}),
                                   query_params={'search': 'content_number1'},
                                   )
   
        self.assertContains(response, self.article_1_query.content, status_code=200, count=1)
        self.assertNotContains(response, self.article_2_query.content, status_code=200)
        self.assertQuerySetEqual(response.context['article_queryset'], [self.article_1_query])
        self.assertTemplateUsed(response, 'notebook/section_detail.html')

    def test_get_articles_with_search_not_exist(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}),
                                   query_params={'search': ''.join('abc' for _ in range(4))},
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['article_queryset'], [])

class CreateArticleSectionView(TestCase):
    """Test create Article"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_section_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_create_articles_not_login_user(self):
        response = self.client.post(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}),
                                   data={"content": "created_name"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/detail-section/{self.section_1.id}/article/',
                            target_status_code=200
                            )

    def test_create_article(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}),
                                   data={"content": "created_name"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}), target_status_code=200)
        self.assertIsNotNone(Article.objects.filter(content='created_name').first())

class ArticleSectionDeleteViewTestCase(TestCase):
    """Test delete Article"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_article_data()
        cls.article_1_query = Article.objects.get(content=f'article_content_number1')
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_delete_article_not_login_user(self):
        response = self.client.post(reverse('notebook:article_delete',kwargs={"pk": self.article_1_query.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/delete-article/{self.article_1_query.id}/',
                            target_status_code=200
                            )
    
    def test_delete_article_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:article_delete',kwargs={"pk": self.article_1_query.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Article.objects.filter(content='article_content_number1').first())

    def test_delete_article_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:article_delete',kwargs={"pk": self.article_1_query.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:show_articles', kwargs={"pk": self.section_1.id}), target_status_code=200)
        self.assertIsNone(Article.objects.filter(content='article_content_number1').first())

class LinksSectionViewTestCase(TestCase):
    """Test detail of section with links"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_links_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')
        cls.link_1_query = Links.objects.get(name='link_name_number1')
        cls.link_2_query = Links.objects.get(name='link_name_number2')
        cls.links_queryset = Links.objects.filter(section=cls.section_1).order_by('id')

    def test_get_links_not_login_user(self):
        response = self.client.get(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/detail-section/{self.section_1.id}/links/',
                            target_status_code=200
                            )
        
    def test_get_links_user_is_owner(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}))
        self.assertContains(response, self.section_1.title, status_code=200, count=1)
        self.assertContains(response, self.section_1.description, status_code=200, count=1)
        self.assertQuerySetEqual(response.context['links_queryset'].order_by('id'), self.links_queryset)
        self.assertEqual(response.context['section_object'], self.section_1)
        self.assertTemplateUsed(response, 'notebook/section_detail.html')
        self.assertTemplateUsed(response, 'notebook/links_list.html')

    def test_get_links_user_not_owner(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.get(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}))

        for link in self.links_queryset:
            with self.subTest(link=link):
                self.assertContains(response, link.name, status_code=200, count=1)
                self.assertContains(response, link.url, status_code=200, count=1)


    def test_get_links_with_search(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}),
                                   query_params={'search': 'name_number1'},
                                   )
   
        self.assertContains(response, self.link_1_query.name, status_code=200, count=1)
        self.assertNotContains(response, self.link_2_query.name, status_code=200)
        self.assertQuerySetEqual(response.context['links_queryset'], [self.link_1_query])
        self.assertTemplateUsed(response, 'notebook/section_detail.html')

    def test_get_links_with_search_not_exist(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.get(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}),
                                   query_params={'search': ''.join('abc' for _ in range(4))},
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['links_queryset'], [])

class CreateLinkSectionView(TestCase):
    """Test create Link"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_section_data()
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_create_links_not_login_user(self):
        response = self.client.post(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}),
                                   data={"name": "created_name", "content": "created_content", "url": "https://cretedurl"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/detail-section/{self.section_1.id}/links/',
                            target_status_code=200
                            )

    def test_create_link(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:show_links', kwargs={"pk": self.section_1.id}),
                                   data={"name": "created_name", "content": "created_content", "url": "http://127.0.0.1:7900/tasks/create/"},
                                   )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:show_links', kwargs={"pk": self.section_1.id}), target_status_code=200)
        self.assertIsNotNone(Links.objects.filter(name='created_name').first())

class LinksSectionDeleteViewTestCase(TestCase):
    """Test delete Link"""
    @classmethod
    def setUpTestData(cls):
        test_utils.create_test_links_data()
        cls.link_1_query = Links.objects.get(name='link_name_number1')
        cls.section_1 = Section.objects.get(title='title_section_number_1')

    def test_delete_link_not_login_user(self):
        response = self.client.post(reverse('notebook:link_delete',kwargs={"pk": self.link_1_query.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/notebook/delete-link/{self.link_1_query.id}/',
                            target_status_code=200
                            )
    
    def test_delete_link_not_owner_user(self):
        self.client.login(username='user_name_2', password='password')
        response = self.client.post(reverse('notebook:link_delete',kwargs={"pk": self.link_1_query.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Links.objects.filter(name='link_name_number1').first())

    def test_delete_link_owner_user(self):
        self.client.login(username='user_name_1', password='password')
        response = self.client.post(reverse('notebook:link_delete',kwargs={"pk": self.link_1_query.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notebook:show_links', kwargs={"pk": self.section_1.id}), target_status_code=200)
        self.assertIsNone(Links.objects.filter(name='link_name_number1').first())

   