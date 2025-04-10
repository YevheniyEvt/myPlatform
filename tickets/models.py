from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField
from django.utils.text import slugify
# Create your models here.

def get_display_name(instance):
    return instance.display_name()

def get_public_id_prefix(instance):
    model_name = instance.__class__.__name__
    return f"{model_name}/{instance.get_display_name()}/"


class TicketLocationChoices(models.TextChoices):
    SALARY = "BKS", "Bookkeepers"
    LOGISTIC_SUPPORT = "LS", "Logistic Supporter"
    HELP_DESK = "IT", "Sys Admin"
    AUDITOR = "AU", "Auditor"
    FACILITY = "FA", "Facility"
    RETAIL = "RA", "Retail"


class Ticket(models.Model):
    tittle = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    reopen_date = models.DateTimeField(null=True, blank=True)

    location = models.CharField(choices=TicketLocationChoices, max_length=50)
    
    creator = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    recipient = models.ManyToManyField(User, through="TicketRecipient", related_name="recipient")
    
    image = CloudinaryField('image',
                                display_name=get_display_name,
                                public_id_prefix=get_public_id_prefix,
    )

    def display_name(self):
        return f"Section-{slugify(self.section.title)}-Image-{slugify(self.image_title)}"
    
    def get_image_url(self):
        if self.image_file is not None:
            return self.image_file.build_url()
        return None


class TicketRecipient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    accepted = models.DateTimeField(auto_now_add=True)

class TicketComment(models.Model):
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, null=True, blank=True)
    action_date = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image',
                                display_name=get_display_name,
                                public_id_prefix=get_public_id_prefix,
    )

    def display_name(self):
        return f"Section-{slugify(self.section.title)}-Image-{slugify(self.image_title)}"
    
    def get_image_url(self):
        if self.image_file is not None:
            return self.image_file.build_url()
        return None
