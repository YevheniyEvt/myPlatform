from django.shortcuts import render, redirect

from django.db.models import Subquery, Q, Count
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from tasks.models import TaskUsers, Task
from tasks.utils import get_users_from_location
from employee.utils import get_user_location
from comunication.models import Articke, ViewArticle
from comunication.utils import can_create_article, get_allowed_articles
from notebook.models import Section, Note


@login_required
def home(request):
    template_name = 'home.html'
    current_user = get_user(request)
    current_user_location = get_user_location(current_user)
    date = timezone.localdate()

    can_create = can_create_article(current_user)

    news_revised_user = get_allowed_articles(current_user).exclude(is_competition=True).filter(is_global=False).annotate(
        revised_user=Count('viewarticle', filter=Q(viewarticle__user=current_user))
    )
 

    competitions = Articke.objects.all().filter(is_competition=True).annotate(
        revised_user=Count('viewarticle', filter=Q(viewarticle__user=current_user))
    )

    global_news = Articke.objects.all().filter(is_global=True).annotate(
        revised_user=Count('viewarticle', filter=Q(viewarticle__user=current_user))
    )[:5]

    my_tasks = current_user.taskusers_set.filter(completed=False, not_accepted=False)

    if current_user_location is not None:
        my_location_users = get_users_from_location(recipients_id=[current_user_location.id], recipients=current_user_location)
        location_task = Task.objects.filter(taskusers__user__in=my_location_users)
        list_task = TaskUsers.objects.filter(task__in=Subquery(location_task.values('pk')), creator=True)
    else:
        list_task = None
    notes = Note.objects.filter(user=current_user)[:5]
    
    search = request.GET.get('search', '')
    sections_query = Section.objects.filter(
        Q(topic__name__icontains=search) |
        Q(title__icontains=search) |
        Q(description__icontains=search)
    )[:8]


    context = {
        "news": news_revised_user,
        "competitions": competitions,
        "global_news": global_news,
        "my_tasks": my_tasks,
        "task_for_my_location": list_task,
        "date": date,
        "notes": notes,
        "sections_query": sections_query,
    }

    return render(request, template_name, context)


