from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import Q
from django.views.generic import View, ListView, DeleteView, UpdateView, CreateView
from django.views.generic.edit import FormMixin


from django.urls import reverse_lazy

from .forms import ArticlesForm
from .models import Articke, Coment, ViewArticle, DeleteHistory
from employee.utils import get_user_store, get_user_location
from .utils import get_allowed_articles, can_create_article, create_coment



@login_required
def create_article(request: HttpRequest):
    curent_user = get_user(request)
    if not curent_user.has_perm('comunication.add_articke'):
        raise Http404
    
    template_name = 'comunication/create_article.html'
    direct_form = ArticlesForm()
    context = {
        "direct_form": direct_form,
    }
    if request.method == "POST":
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = curent_user
            form.instance.location = get_user_location(curent_user)
            form.save()
            return redirect("home")
    return render(request, template_name, context)

@login_required
def news_list(request: HttpRequest):
    search = request.GET.get('search', '')
    curent_user = get_user(request)
    news = get_allowed_articles(curent_user).exclude(is_competition=True).filter(
        Q(title__icontains=search) |
        Q(content__icontains=search)
    )
    template_name = "comunication/list_article.html"
    title = "News"
    context = {
        "articles": news,
        "title": title,
    }
    return render(request, template_name, context)

@login_required
def global_news_list(request:HttpRequest):
    search = request.GET.get('search', '')
    global_news = Articke.objects.all().filter(is_global=True).filter(
        Q(title__icontains=search) |
        Q(content__icontains=search)
    )
    template_name = "comunication/list_article.html"
    context = {
        "articles": global_news,
    }
    return render(request, template_name, context)


@login_required
def competition_list(request: HttpRequest):
    search = request.GET.get('search', '')
    competition = Articke.objects.all().filter(is_competition=True).filter(
        Q(title__icontains=search) |
        Q(content__icontains=search)
    )
    template_name = "comunication/list_article.html"
    title = "Competitions"
    context = {
        "articles": competition,
        "title": title,
    }
    return render(request, template_name, context)

@login_required
def detail_article(request: HttpRequest, article_id):
    template_name = "comunication/detail_article.html"
    article = get_object_or_404(Articke, id=article_id)
    curent_user = get_user(request)
    if request.method == "GET":
        ViewArticle.objects.get_or_create(
           article=article,
           user=curent_user,
           view=True
        )
    allowed_articles = get_allowed_articles(curent_user)
    if article in allowed_articles or article.is_competition == True:
        coments = Coment.objects.filter(article=article)
        context = {
            "object": article,
            "coments": coments,
            "user": curent_user,
        }
        if request.method == "POST":
            create_coment(request=request, object=article) 
            return redirect("comunication:detail_article", article_id=article_id)
        return render(request, template_name, context)
    return redirect("home")

@login_required
def update_article(request: HttpRequest, article_id):
    template_name = "comunication/update_article.html"
    article =  get_object_or_404(Articke, id=article_id)
    article_data = Articke.objects.filter(id=article_id)
    context = {
        "article": article
    }
    if request.method == "POST":
        form = ArticlesForm(request.POST, initial=article_data.values()[0])
        if not form.has_changed():
            return redirect("comunication:detail_article", article_id=article_id)
        elif form.is_valid():
            form_data = form.cleaned_data
            updated_field = {field: form_data[field] for field in form.changed_data}
            Articke.objects.filter(id=article.id).update(**updated_field)
            return redirect("comunication:detail_article", article_id=article_id)
    return render(request, template_name, context)

@login_required
def delete_article(request: HttpRequest, article_id):
    current_user = get_user(request)
    article = Articke.objects.get(id=article_id)
    if request.method == "POST":
        content = f"user: {current_user}, delete article: {article.title}, with content:{article.content[:50]}."
        DeleteHistory.objects.create(user=current_user, content=content, article=True)
        article.delete()
    return redirect("home")


def delete_coment(request: HttpRequest, coment_id):
    current_user = get_user(request)
    coment = Coment.objects.get(id=coment_id)
    article_id = coment.article.id
    if request.method == 'POST':
        content = f"user: {current_user}, delete comment from article: {coment.article.title}, with content:{coment.content}."
        DeleteHistory.objects.create(user=current_user, content=content, comment=True)
        coment.delete()
    return redirect("comunication:detail_article", article_id=article_id)



  
