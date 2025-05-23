from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from comunication.models import Articke, ViewArticle, Coment, DeleteHistory
from comunication.utils import get_allowed_articles


class CreateArticleTestCase(TestCase):
    fixtures = ["test_data"]

    def test_create_article_user_not_login(self):
        response=self.client.post(reverse('comunication:create_article'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                            f'{reverse('user:login')}?next=/comunication/article/create/',
                            target_status_code=200,
                            )

    def test_create_article_user_login(self):
        self.client.login(username='admin', password='1234')
        response=self.client.post(reverse('comunication:create_article'),
                                  data={
                                    'owner': User.objects.get(username='admin'),
                                    'title': 'Hello test',
                                    'content': 'Hello test',
                                    'is_local': True,
                                    'is_global': True,
                                    'is_competition': False,
                                    'permission': 'all',
                                  })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), target_status_code=200)
        self.assertIsNotNone(Articke.objects.filter(title='Hello test').first())


class UpdateArticleTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.user_article = Articke.objects.filter(owner=self.user).first()
        self.not_user_article = Articke.objects.exclude(owner=self.user).first()

    def test_update_article_not_login_user(self):
        response = self.client.post(reverse('comunication:update_article',kwargs={"pk": self.user_article.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'{reverse('user:login', )}?next=/comunication/article/update/{self.user_article.id}/',
                             target_status_code=200,
                             )

    def test_user_owner_article_get_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('comunication:update_article', kwargs={'pk': self.user_article.id}))
        self.assertEqual(response.status_code, 200)

    def test_user_not_owner_article_get_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('comunication:update_article', kwargs={'pk': self.not_user_article.id}))
        self.assertEqual(response.status_code, 404)

    def test_user_owner_article_update(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('comunication:update_article', kwargs={'pk': self.user_article.id}),
                                    data={'title': 'Hello Test', 'content': 'It is Test', 'permission': 'all'}
                                    )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('comunication:detail_article', kwargs={'pk': self.user_article.id}),
                             target_status_code=200
                             )
        
        new_article = Articke.objects.get(id=self.user_article.id)
        self.assertEqual(new_article.title, 'Hello Test')
        self.assertEqual(new_article.content, 'It is Test')

    def test_user_not_owner_article_update(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('comunication:update_article', kwargs={'pk': self.not_user_article.id}),
                                    data={'title': 'sssHello Test', 'content': 'It is Test', 'permission': 'all'}
                                    )
        self.assertEqual(response.status_code, 404)

        new_article = Articke.objects.get(id=self.user_article.id)
        self.assertNotEqual(new_article.title, 'Hello Test')
        self.assertNotEqual(new_article.content, 'It is Test')


class DeleteArticleTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.user_article = Articke.objects.filter(owner=self.user).first()
        self.not_user_article = Articke.objects.exclude(owner=self.user).first()

    def test_delete_article_not_login_user(self):
        response = self.client.post(reverse('comunication:delete_article',kwargs={"pk": self.user_article.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'{reverse('user:login', )}?next=/comunication/article/delete/{self.user_article.id}/',
                             target_status_code=200
                             )
    
    def test_delete_article_not_owner_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('comunication:delete_article',kwargs={"pk": self.not_user_article.id}))
        self.assertEqual(response.status_code, 404)
        self.assertIsNotNone(Articke.objects.filter(id=self.not_user_article.id))

    def test_delete_article_owner_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('comunication:delete_article',kwargs={"pk": self.user_article.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'), target_status_code=200)
        self.assertIsNone(Articke.objects.filter(id=self.user_article.id).first())

        del_history = DeleteHistory.objects.filter(content__icontains=self.user_article.title).first()
        self.assertIsNotNone(del_history)


class DetailArticleTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user_all_permission = User.objects.get(username='admin')
        self.article_2 = Articke.objects.filter(owner=self.user_all_permission).first()        
    
    def test_detail_article_not_login_user(self):
        response = self.client.get(reverse('comunication:detail_article', kwargs={"pk": self.article_2.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'{reverse('user:login')}?next=/comunication/{self.article_2.id}/',
                             target_status_code=200,
                             )

    def test_detail_article_in_allowed_article(self):
        self.client.force_login(self.user_all_permission)
        article = get_allowed_articles(self.user_all_permission)[0]
        comments = Coment.objects.filter(article=article)
        response = self.client.get(reverse('comunication:detail_article', kwargs={"pk": article.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], article)
        self.assertTemplateUsed(response, "comunication/detail_article.html")

        article_view = ViewArticle.objects.filter(user=response.wsgi_request.user, article=article).first()
        self.assertIsNotNone(article_view)
        self.assertTrue(article_view.view)
        self.assertQuerySetEqual(response.context['comments'], comments, ordered=False)
        
    def test_detail_article_not_in_allowed_article(self):
        user = User.objects.filter(storeemployee__isnull=False).first()
        article_allowed = get_allowed_articles(user)
        article = Articke.objects.all().difference(article_allowed)[0]
        self.client.force_login(user)
        response = self.client.get(reverse('comunication:detail_article', kwargs={"pk": article.id}))
        self.assertEqual(response.status_code, 404)


class GlobalNewsListTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.global_news = Articke.objects.all().filter(is_global=True)
        self.user_district_permission = User.objects.filter(storeemployee__isnull=False).first()
        self.search = 'quis'

    def test_get_global_news_article(self):
        self.client.force_login(self.user_district_permission)
        response = self.client.get(reverse('comunication:global_news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], self.global_news, ordered=False)

    def test_get_global_news_article_with_search(self):
        article_with_search = self.global_news.filter(Q(title__icontains=self.search) | Q(content__icontains=self.search))

        self.client.force_login(self.user_district_permission)
        response = self.client.get(reverse('comunication:global_news_list'), query_params={'search': self.search})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], article_with_search, ordered=False)


class NewsListTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user_district_permission = User.objects.filter(storeemployee__isnull=False).first()
        self.news = get_allowed_articles(self.user_district_permission).exclude(is_competition=True)
        self.search = 'quis'

    def test_get_news_article(self):
        self.client.force_login(self.user_district_permission)
        response = self.client.get(reverse('comunication:list_article'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], self.news, ordered=False)

    def test_get_news_article_with_search(self):
        article_with_search = self.news.filter(Q(title__icontains=self.search) | Q(content__icontains=self.search))

        self.client.force_login(self.user_district_permission)
        response = self.client.get(reverse('comunication:list_article'), query_params={'search': self.search})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], article_with_search, ordered=False)


class CompetitionListTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user_district_permission = User.objects.filter(storeemployee__isnull=False).first()
        self.competition = Articke.objects.all().filter(is_competition=True)
        self.search = 'quis'
        
    def test_get_competition_article(self):
        self.client.force_login(self.user_district_permission)
        response = self.client.get(reverse('comunication:competition_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], self.competition, ordered=False)

    def test_get_competition_article_with_search(self):
        article_with_search = self.competition.filter(Q(title__icontains=self.search) | Q(content__icontains=self.search))

        self.client.force_login(self.user_district_permission)
        response = self.client.get(reverse('comunication:competition_list'), query_params={'search': self.search})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['articles'], article_with_search, ordered=False)


class CreateArticleCommentTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.user_article = Articke.objects.filter(owner=self.user).first()

    def test_create_article_comment_not_login_user(self):
        response = self.client.post(reverse('comunication:detail_article',kwargs={"pk": self.user_article.id}),
                                    data={'content': 'Hello test comment'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'{reverse('user:login', )}?next=/comunication/{self.user_article.id}/',
                             target_status_code=200,
                             )

    def test_create_comment(self):
        article = Articke.objects.first()
        user = article.owner
        self.client.force_login(user)
        response = self.client.post(reverse('comunication:detail_article', kwargs={'pk': article.id}),
                                    data={'content': 'Hello'})

        self.assertEqual(response.status_code, 302)
        comment = Coment.objects.filter(content='Hello').first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.article, article)
        self.assertEqual(comment.owner, user)

    def test_create_comment_not_allowed_article(self):
        user = User.objects.filter(storeemployee__isnull=False).first()
        article_allowed = get_allowed_articles(user)
        article = Articke.objects.all().difference(article_allowed)[0]
        self.client.force_login(user)
        response = self.client.post(reverse('comunication:detail_article', kwargs={'pk': article.id}),
                                    data={'content': 'Hello'})
        self.assertEqual(response.status_code, 404)

class DeleteArticleCommentTestCase(TestCase):
    fixtures = ["test_data"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.article = Articke.objects.filter(is_competition=True).first()
        self.user_comment = Coment.objects.create(owner=self.user,
                                                article=self.article,
                                                content='Hello',
                                                )
        self.not_user_comment = Coment.objects.exclude(owner=self.user).first()

    def test_delete_article_comment_not_login_user(self):
        response = self.client.post(reverse('comunication:delete_coment',kwargs={"pk": self.user_comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'{reverse('user:login', )}?next=/comunication/delete/coment/{self.user_comment.id}/',
                             target_status_code=200,
                             )

    def test_delete_comment_user_owner(self):
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('comunication:delete_coment', kwargs={"pk": self.user_comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(Coment.objects.filter(id=self.user_comment.id).first())
        
        del_history = DeleteHistory.objects.filter(content__icontains='Hello').first()
        self.assertIsNotNone(del_history)
        