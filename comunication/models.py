from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from cloudinary.models import CloudinaryField

from tasks.models import Task

# Create your models here.
def get_display_name(instance):
    return instance.get_display_name()

def get_public_id_prefix(instance):
    model_name = instance.__class__.__name__
    return f"{model_name}/{instance.get_display_name()}/"

class PermissionChoise(models.TextChoices):
    DISTRIC = 'distric'
    REGION = 'region'
    ALL = 'all'




class Articke(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    is_local = models.BooleanField(default=True)
    is_global = models.BooleanField(default=False)
    is_competition = models.BooleanField(default=False)
    permission = models.CharField(max_length=50, choices=PermissionChoise, default=PermissionChoise.ALL)
    location = models.CharField(max_length=50, blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True,
                            display_name=get_display_name,
                            public_id_prefix=get_public_id_prefix,
                            )

    def __str__(self):
        return self.title
    
    @property
    def revised(self):
        return self.viewarticle_set.filter(view=True)
    
    def get_display_name(self):
        return f"Article-{slugify(self.title)}-Owner-{self.owner.username}"
    
    
    def get_image_url(self):
        if self.image is not None:
            return self.image.build_url(
                width=1000,
                height=300,
                crop="pad",
                background="gen_fill:ignore-foreground_true",
                quality="auto"
                )
        else:
            return None

    
class ViewArticle(models.Model):
    """User view article or not"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articke, on_delete=models.CASCADE)
    view = models.BooleanField(default=False)



class Coment(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articke, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)



class DeleteHistory(models.Model):
    """All deleted objects"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    article = models.BooleanField(default=False)
    task = models.BooleanField(default=False)
    comment = models.BooleanField(default=False)
    note = models.BooleanField(default=False)
    time_action = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-time_action"]



class NotesOld(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f'{self.date} "{self.text[0:50]}..."'
    
    class Meta:
        ordering = ['-date']