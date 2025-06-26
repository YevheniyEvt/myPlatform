from django.db import models

# Create your models here.

class Address(models.Model):
    city = models.CharField()
    country = models.CharField()

class Links(models.Model):
    name = models.CharField()
    url = models.URLField()

class AboutMe(models.Model):
    first_name = models.CharField()
    second_name = models.CharField()
    descriptions = models.TextField()
    short_description = models.CharField(blank=True, null=True)
    email = models.EmailField()
    address = models.ForeignKey(to=Address, on_delete=models.CASCADE)
    links = models.ForeignKey(to=Links, on_delete=models.CASCADE)


class Description(models.Model):
    text = models.TextField()

class Tags(models.Model):
    name = models.CharField()
    descriptions = models.ForeignKey(to=Description, on_delete=models.CASCADE)

class Projects(models.Model):
    name = models.CharField()
    descriptions = models.TextField()
    instruments = models.TextField(blank=True, null=True)
    tags = models.ForeignKey(to=Tags, on_delete=models.CASCADE, blank=True, null=True)
    links = models.ForeignKey(to=Links, on_delete=models.CASCADE, blank=True, null=True)


class Course(models.Model):
    name = models.CharField()
    descriptions = models.TextField()

class Lection(models.Model):
    name = models.CharField()
    descriptions = models.TextField()

class Book(models.Model):
    name = models.TextField()
    author = models.CharField()
    
class Education(models.Model):
    descriptions = models.TextField()
    courses = models.ForeignKey(to=Course, on_delete=models.CASCADE, blank=True, null=True)
    lections = models.ForeignKey(to=Lection, on_delete=models.CASCADE, blank=True, null=True)
    books = models.ForeignKey(to=Book, on_delete=models.CASCADE, blank=True, null=True)


class WorkFlow(models.Model):
    name = models.TextField()

class Instrument(models.Model):
    name = models.CharField()

class Skills(models.Model):
    workflows = models.ForeignKey(to=WorkFlow, on_delete=models.CASCADE, blank=True, null=True)
    instruments = models.ForeignKey(to=Instrument, on_delete=models.CASCADE, blank=True, null=True)


class Hobbies(models.Model):
    descriptions = models.TextField()



