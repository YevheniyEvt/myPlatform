from about.models import (Address, Links, AboutMe,
                     Description, Tag, Projects,
                     Course, Lection, Book, Education,
                     WorkFlow, Instrument, Skills,
                     Hobbies, IconClass)


def create_test_data_about() -> AboutMe:
    
    about = AboutMe.objects.create(
        first_name='First name',
        second_name='Second name',
        descriptions='Test descriptions AboutMe '*4,
        short_description='Test short description AboutMe',
        email='Test@mail.com',
    )
    Address.objects.create(
        city='City',
        country='Country',
        about=about
    )
    Links.objects.create(
        name='resume',
        url='http://127.0.0.1:8000/about',
        about=about
    )
    for i in range(3):
        icon = IconClass.objects.create(
            name=f'Test{i} IconClass ',
            css_class=f'css_class{i} AboutMe'
        )
        Links.objects.create(
            name=f'Test{i} AboutMe',
            url=f'http://127.0.0.1:8000/AboutMe{i}',
            icon=icon,
            about=about
        )
    return about

def create_test_data_projects() -> Projects:
    project = Projects.objects.create(
        name='Test Projects',
        descriptions='Test descriptions Projects '*3,
        instruments='Test instruments Projects '*2

    )
    Links.objects.create(
        name='github',
        url='http://127.0.0.1:8000/Projects',
        project=project
    )
    for i in range(3):
        tag = Tag.objects.create(
            name=f"Test{i} Tag",
            project=project
        )
        for i in range(2):
            Description.objects.create(
                text='Test text Description'*3,
                tag=tag
            )
    return project

def create_test_data_education() -> Education:
    education = Education.objects.create(
        descriptions='Test descriptions Education'
    )
    Course.objects.create(
        name='Test name Course',
        descriptions='Test Course '*2,
        education=education
    )
    Lection.objects.create(
        name='Test name Lection',
        descriptions='Test Lection '*2,
        education=education
    )
    Book.objects.create(
        name='Test Book',
        author='Test author',
        education=education
    )
    return education

def create_test_data_skills() -> Skills:
    skills = Skills.objects.create(
        descriptions='Test descriptions Skills'
    )
    
    for i in range(3):
        WorkFlow.objects.create(
            name=f"Test{i} WorkFlow",
            skills=skills
        )
        icon = IconClass.objects.create(
            name=f'Test{i} IconClass',
            css_class=f'css_class{i} Instrument'
        )
        Instrument.objects.create(
            name=f"Test{i} Instrument",
            skills=skills,
            icon=icon
        )
    return skills

def create_test_data_hobbies() -> Hobbies:
    hobbies = Hobbies.objects.create(
        descriptions='Test Hobbies '*2
    )
    return hobbies