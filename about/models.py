from django.db import models

# Create your models here.

class IconClass(models.Model):
    name = models.CharField()
    css_class = models.CharField()

    def __str__(self):
        return self.name
    

class AboutMe(models.Model):
    first_name = models.CharField()
    second_name = models.CharField()
    descriptions = models.TextField()
    short_description = models.CharField(blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.first_name
    
    @property
    def contact_links(self):
        return self.links_set.exclude(name='resume').all()
    
    @property
    def resume_url(self):
        return self.links_set.filter(name='resume').first().url
    

class Address(models.Model):
    city = models.CharField()
    country = models.CharField()
    about = models.OneToOneField(to=AboutMe, on_delete=models.CASCADE)


class Projects(models.Model):
    name = models.CharField()
    descriptions = models.TextField()
    instruments = models.TextField(blank=True, null=True)
    order = models.BigIntegerField(default=0)


    def __str__(self):
        return self.name
    
    @property
    def tags(self):
        return self.tag_set.all()
    
    @property
    def github_url(self):
        return self.links_set.filter(name='github').first().url
    
    
class Tag(models.Model):
    name = models.CharField()
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Проєкт: {self.project})"
    
    @property
    def descriptions(self):
        return self.description_set.all()

class Description(models.Model):
    text = models.TextField()
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)


class Links(models.Model):
    name = models.CharField()
    url = models.URLField()
    icon = models.ForeignKey(to=IconClass, on_delete=models.CASCADE, blank=True, null=True)
    about = models.ForeignKey(to=AboutMe, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    descriptions = models.TextField()

    def __str__(self):
        return f"{self.descriptions[:25]}..."
    
    @property
    def courses(self):
        return self.course_set.all()

    @property
    def lections(self):
        return self.lection_set.all()
    
    @property
    def books(self):
        return self.book_set.all()
    
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
    
    @property
    def workflows(self):
        return self.workflow_set.all()
    
    @property
    def instruments(self):
        return self.instrument_set.all()

class WorkFlow(models.Model):
    name = models.TextField()
    skills = models.ForeignKey(to=Skills, on_delete=models.CASCADE, blank=True, null=True)

class Instrument(models.Model):
    name = models.CharField()
    icon = models.OneToOneField(to=IconClass, on_delete=models.CASCADE)
    skills = models.ForeignKey(to=Skills, on_delete=models.CASCADE, blank=True, null=True)

    
class Hobbies(models.Model):
    descriptions = models.TextField()

    def __str__(self):
        return f"{self.descriptions[:25]}..."



