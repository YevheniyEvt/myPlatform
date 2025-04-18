from django.db.models import Q
from django.contrib.auth import get_user

from employee.models import District, Region
from employee.utils import get_user_district, get_user_store

from tasks.models import Task
from .forms import ComentForm
from .models import Articke, PermissionChoise, Coment


def get_allowed_articles(curent_user):
    location = get_user_district(curent_user)
    if isinstance(location, District):
        region = location.region
        articles = Articke.objects.filter(
            Q(permission=PermissionChoise.ALL) |
            (Q(permission=PermissionChoise.DISTRIC) & Q(location=location)) |
            (Q(permission=PermissionChoise.REGION) & Q(location=region))
            )
        return articles
    elif isinstance(location, Region):
        articles = Articke.objects.all()
        return articles
    return Articke.objects.all()
    

def can_create_article(curent_user):
    if get_user_store(curent_user) is not None:
        return False
    return True

def create_coment(request, object_creation):
    
    form = ComentForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        owner = get_user(request)
        content = form_data.get("content")
        if isinstance(object_creation, Articke):
            
            Coment.objects.create(
                owner=owner,
                article=object_creation,
                content=content
            )
        if isinstance(object_creation, Task):
             Coment.objects.create(
                owner=owner,
                task=object_creation,
                content=content
            )
             
