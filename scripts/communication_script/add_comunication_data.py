
import random
from collections import deque

from django.contrib.auth.models import User

from comunication.models import Articke, ViewArticle, Coment
from scripts.communication_script.data import TEXT_FOR_ARTICLE, DISTRICTS


COUNT_ARTICLES = 20
COUNT_COMMENT = 2

PERMISSION =  [
    'distric',
    'region',
    'all']
LOCATION = ['District', 'Region', 'Region']
DISTRICTS = deque(DISTRICTS)

def crete_articles():
    users = deque(User.objects.exclude(storeemployee__isnull=False))
    locations = deque(LOCATION)
    index = deque([True, False, False])
    for i in range(COUNT_ARTICLES):
        Articke.objects.create(
            owner=users[0],
            title=' '.join(TEXT_FOR_ARTICLE[i + 3:10 + i]),
            content=' '.join(TEXT_FOR_ARTICLE[i:15]),
            is_local=index[0],
            is_global=index[1],
            is_competition=index[2],
            permission=random.choice(PERMISSION),
            location=DISTRICTS[0],
        )
        users.rotate()
        locations.rotate()
        index.rotate()
        DISTRICTS.reverse()

def create_article_is_view():
    users = deque(User.objects.exclude(storeemployee__isnull=False))
    articles = deque(Articke.objects.all())

    for _ in range(int(COUNT_ARTICLES/2)):
        ViewArticle.objects.create(
            user=users[0],
            article=articles[0],
            view=True
        )   
        users.rotate()
        articles.rotate()


def create_article_comments():
    users = deque(User.objects.all())
    articles = deque(Articke.objects.all())

    for article in articles:
        for i in range(COUNT_COMMENT):
            Coment.objects.create(
                owner=users[0],
                article=article,
                content=' '.join(TEXT_FOR_ARTICLE[i*3:3])
            )
        users.rotate()



def database_is_empty():
    return not Articke.objects.first()

def communication_run():
    if database_is_empty():
        print('Start create article data...', end=' ')
        crete_articles()
        create_article_is_view()
        create_article_comments()
        print('Ok')
    else:
        print('Articke data - Ok')

