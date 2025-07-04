from django.test import TestCase
from django.urls import reverse

from .add_data import *


class AboutContextInHTML(TestCase):

    def setUp(self):
        self.about = create_test_data_about()
        self.education = create_test_data_education(self.about)
        self.projects = create_test_data_projects(self.about)
        self.skills = create_test_data_skills(self.about)
        self.hobbies = create_test_data_hobbies(self.about)

    def test_about_context(self):
        response = self.client.get(reverse('about:about_page'))
        self.assertContains(response, self.about.first_name)
        self.assertContains(response, self.about.second_name)
        self.assertContains(response, self.about.descriptions)
        self.assertContains(response, self.about.short_description)
        self.assertContains(response, self.about.email)

        links = self.about.links_set.all()
        for link in links:
            with self.subTest(link=link):
                self.assertContains(response, link.url)
                if link.icon is not None:
                    self.assertContains(response, link.icon.css_class)

    def test_projects_context(self):
        response = self.client.get(reverse('about:about_page'))
        self.assertContains(response, self.projects.name)
        self.assertContains(response, self.projects.descriptions)
        self.assertContains(response, self.projects.instruments)
        
        links = self.projects.links_set.all()
        for link in links:
            with self.subTest(link=link):
                self.assertContains(response, link.url)

        tags = self.projects.tag_set.all()
        for tag in tags:
            with self.subTest(tag=tag):
                self.assertContains(response, tag.name)
                descriptions = tag.description_set.all()
                for description in descriptions:
                    self.assertContains(response, description.text)

    def test_education_context(self):
        response = self.client.get(reverse('about:about_page'))
        self.assertContains(response, self.education.descriptions)

        courses = self.education.course_set.all()
        for course in courses:
            with self.subTest(course=course):
                self.assertContains(response, course.name)
                self.assertContains(response, course.descriptions)

        lections = self.education.lection_set.all()
        for lection in lections:
            with self.subTest(lection=lection):
                self.assertContains(response, lection.name)
                self.assertContains(response, lection.descriptions)

        books = self.education.book_set.all()
        for book in books:
            with self.subTest(book=book):
                self.assertContains(response, book.name)
                self.assertContains(response, book.author)     

    def test_skills_context(self):
        response = self.client.get(reverse('about:about_page'))
        self.assertContains(response, self.skills.descriptions) 
        
        workflows = self.skills.workflow_set.all()
        for workflow in workflows:
            with self.subTest(workflow=workflow):
                self.assertContains(response, workflow.name)

        instruments = self.skills.instrument_set.all()
        for instrument in instruments:
            with self.subTest(instrument=instrument):
                self.assertContains(response, instrument.icon.css_class)

    def test_hobbies_context(self):
        response = self.client.get(reverse('about:about_page'))
        self.assertContains(response, self.hobbies.descriptions) 