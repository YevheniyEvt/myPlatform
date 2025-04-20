from collections import deque

from django.contrib.auth.models import User

from notebook.models import Topic, Section, Code, Article, Links, Note
from scripts.notebook_script import data


COUNT_TOPICS = 10
COUNT_SECTION = 6
COUNT_COD_EXAMPLE = 5
COUNT_ARTICLE = 5
COUNT_LINKS = 10
COUNT_NOTE = 10

USERS = User.objects.all()

def create_topics():
    users = deque(USERS)
    topic_data = deque(data.TEXT)
    for _ in range(COUNT_TOPICS):
        Topic.objects.create(
            user=users[0],
            name=topic_data[0],
            short_description=topic_data[0:2]
        )
        topic_data.rotate()
        users.rotate()

def create_section():
    users = deque(USERS)
    topics = Topic.objects.all()
    section_data = deque(data.TEXT)
    for topic in topics:
        for _ in COUNT_SECTION:
            Section.objects.create(
                owner=users[0],
                topic=topic,
                title=section_data[0:2],
                description=section_data[2:5]

            )
            users.rotate()
            section_data.rotate()

def create_code():
    users = deque(USERS)
    sections = Section.objects.all()
    cod_data = deque(data.COD_EXAMPLE)
    for section in sections:
        for _ in COUNT_COD_EXAMPLE:
            Code.objects.create(
                owner=users[0],
                section=section,
                content=cod_data[0]
            )
            cod_data.rotate()
        users.rotate()

def create_links():
    sections = Section.objects.all()
    link_data = deque(data.LINKS_EXAMPLE)
    text = deque(data.TEXT)
    for section in sections:
        for _ in COUNT_COD_EXAMPLE:
            Code.objects.create(
                section=section,
                name=text[0],
                content=text[0:2],
                url=link_data[0]
            )
            link_data.rotate()

def create_note():
    users = deque(USERS)
    text = deque(data.TEXT)
    for user in users:
        for _ in COUNT_NOTE:
            Note.objects.create(
                user=user,
                text=text[:10]
            )

def database_is_empty():
    return not Topic.objects.first()

def notebook_run():
    if database_is_empty():
        print('Start create notebook data...', end=' ')
        create_topics()
        create_section()
        create_code()
        create_links()
        create_note()
        print('Ok')
    else:
        print('Notebook data - Ok')
