from django.db import models

# Create your models here.
class AboutMe(models.Model):
    first_name = models.CharField()
    second_name = models.CharField()
    descriptions = models.TextField()
    short_description = models.CharField(blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.first_name

class Address(models.Model):
    city = models.CharField()
    country = models.CharField()
    about = models.OneToOneField(to=AboutMe, on_delete=models.CASCADE)


class Projects(models.Model):
    name = models.CharField()
    descriptions = models.TextField()
    instruments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField()
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Проєкт: {self.project})"

class Description(models.Model):
    text = models.TextField()
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)


class Links(models.Model):
    name = models.CharField()
    url = models.URLField()
    about = models.ForeignKey(to=AboutMe, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE, blank=True, null=True)


class Education(models.Model):
    descriptions = models.TextField()

    def __str__(self):
        return f"{self.descriptions[:25]}..."

class Course(models.Model):
    name = models.CharField()
    descriptions = models.TextField()
    education = models.ForeignKey(to=Education, on_delete=models.CASCADE)

class Lection(models.Model):
    name = models.CharField()
    descriptions = models.TextField()
    education = models.ForeignKey(to=Education, on_delete=models.CASCADE)

class Book(models.Model):
    name = models.TextField()
    author = models.CharField()
    education = models.ForeignKey(to=Education, on_delete=models.CASCADE)
    

class Skills(models.Model):
    descriptions = models.TextField()
    
    def __str__(self):
        return f"{self.descriptions[:25]}..."

class WorkFlow(models.Model):
    name = models.TextField()
    skills = models.ForeignKey(to=Skills, on_delete=models.CASCADE, blank=True, null=True)

class Instrument(models.Model):
    name = models.CharField()
    skills = models.ForeignKey(to=Skills, on_delete=models.CASCADE, blank=True, null=True)

    
class Hobbies(models.Model):
    descriptions = models.TextField()

    def __str__(self):
        return f"{self.descriptions[:25]}..."



