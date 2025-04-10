from django.contrib.auth.models import User

from ..models import Topic, Section, Code, Article, Links, Image, Note
# Create your tests here.

def create_test_users_data():
    for number in range(1,3):
        User.objects.create_user(
            username=f'user_name_{number}',
            password='password',
            )

def create_test_topic_data():
    create_test_users_data()

    for number in range(1,3):
        user = User.objects.get(
            username=f'user_name_{number}'
            )
        Topic.objects.create(
            user=user ,
            name=f'topic_name_{number}',
            short_description=f'topic short_description{number}',
            )

def create_test_section_data():
    create_test_topic_data()

    for number in range(1,3):
        user = User.objects.get(
            username=f'user_name_{number}'
            )
        topic = Topic.objects.get(
            name=f'topic_name_{number}'
            )
        Section.objects.create(
            topic=topic,
            owner=user,
            title=f'title_section_number_{number}',
            description=f'section description_number_{number}',
        )

def create_test_code_data():
    create_test_section_data()
    for number in range(1,3):
        user = User.objects.get(
            username=f'user_name_{number}'
            )
        section = Section.objects.get(
            title=f'title_section_number_{number}',
        )
        Code.objects.create(
            section=section,
            owner=user,
            content=f'code_content_number{number}'

        )

def create_test_article_data():
    create_test_section_data()
    for number in range(1,3):
        user = User.objects.get(
            username=f'user_name_{number}'
            )
        section = Section.objects.get(
            title=f'title_section_number_{number}',
        )
        Article.objects.create(
            section=section,
            owner=user,
            content=f'article_content_number{number}'

        )

def create_test_links_data():
    create_test_section_data()
    for number in range(1,3):
        user = User.objects.get(
            username=f'user_name_{number}'
            )
        section = Section.objects.get(
            title=f'title_section_number_{number}',
        )
        Links.objects.create(
            section=section,
            name=f'link_name_number{number}',
            content=f'link_content_number{number}',
            url=f"https://docs.python.org/{number}"
        )

def create_test_note_data():
    create_test_users_data()

    for number in range(1,3):
        user = User.objects.get(
            username=f'user_name_{number}'
            )
        for note_number in range(1,12):
            Note.objects.create(
                user=user ,
                text=f'note_{note_number}_text_{number}',
                )
