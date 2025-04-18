from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import Q
from django.views.generic import View, ListView, DeleteView, UpdateView, CreateView, DetailView, FormView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic.detail import SingleObjectMixin

from django.urls import reverse_lazy

from .forms import ArticlesForm
from .models import Articke, Coment, ViewArticle, DeleteHistory
from employee.utils import get_user_store, get_user_location
from .utils import get_allowed_articles, can_create_article, create_coment
from .forms import ComentForm

class CreateArticle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ArticlesForm
    success_url = reverse_lazy('home')
    template_name = 'comunication/create_article.html'
    permission_required  = 'comunication.add_articke'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.location = get_user_location(self.request.user)
        return super().form_valid(form)


class UpdateArticle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Articke
    form_class = ArticlesForm
    template_name = "comunication/update_article.html"
    permission_required  = 'comunication.update_articke'
    context_object_name = 'article'
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('comunication:detail_article',
                               kwargs={"pk": self.get_object().id})


class DeleteArticle(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Articke
    success_url = reverse_lazy('home')
    permission_required  = 'comunication.delete_articke'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def form_valid(self, *args, **kwargs):
        content = f"user: {self.request.user}, delete article: {self.object.title}, with content:{self.object.content[:50]}."
        DeleteHistory.objects.create(user=self.request.user, content=content, article=True)
        return super().form_valid(*args, **kwargs)


class CreateCommentView(CreateView):
    model = Articke
    form_class = ComentForm
    
    def get_success_url(self):
        return reverse_lazy("comunication:detail_article", kwargs={'pk': self.article.id})
    
    def form_valid(self, form):
        self.article = self.get_object()
        form.instance.article = self.article 
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DetailArticleView(DetailView):
    model = Articke
    context_object_name = 'article'
    template_name = "comunication/detail_article.html"

    def get_queryset(self):
        allowed_articles = get_allowed_articles(self.request.user)
        return allowed_articles
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        if article:
            ViewArticle.objects.get_or_create(
                article=article,
                user=self.request.user,
                view=True
            )
        comments = Coment.objects.filter(article=article)
        context['comments'] = comments
        return context

class ArticleCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        view = CreateCommentView.as_view()
        return view(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        view = DetailArticleView.as_view()
        return view(request, *args, **kwargs)
    

@login_required
def detail_article(request: HttpRequest, pk):
    template_name = "comunication/detail_article.html"
    article = Articke.objects.get(id=pk)
    curent_user = request.user

    
    allowed_articles = get_allowed_articles(curent_user)
    if article in allowed_articles or article.is_competition == True:
        coments = Coment.objects.filter(article=article)
        context = {
            "article": article,
            "coments": coments,
            "user": curent_user,
        }
        if request.method == "GET":
            ViewArticle.objects.get_or_create(
                article=article,
                user=curent_user,
                view=True
            )
            return render(request, template_name, context)
        
        if request.method == "POST":
            create_coment(request=request, object_creation=article)
            return redirect("comunication:detail_article", pk=pk)
    else:
        return redirect("home")


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
def delete_coment(request: HttpRequest, pk):
    current_user = request.user
    coment = Coment.objects.filter(id=pk, owner=current_user).first()
    article_id = coment.article.id
    if request.method == 'POST':
        content = f"user: {current_user}, delete comment from article: {coment.article.title}, with content:{coment.content}."
        DeleteHistory.objects.create(user=current_user, content=content, comment=True)
        coment.delete()
    return redirect("comunication:detail_article", pk=article_id)





  #####################################################3#########################
# Old function (did not used. There are class_view)

@login_required
def create_article(request: HttpRequest):
    """Old function. Use CreateArticle.as_view()"""
    curent_user = get_user(request)
    if not curent_user.has_perm('comunication.add_articke'):
        raise Http404
    
    template_name = 'comunication/create_article.html'

    if request.method == "POST":
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.cleaned_data
            article['owner'] = curent_user
            article['location'] = get_user_location(curent_user)
            Articke.objects.create(**article)
            return redirect("home")
    else:
        form = ArticlesForm()
    context = {
        "form": form,
    }
    return render(request, template_name, context)

@login_required
def update_article(request: HttpRequest, article_id):
    """Old function. Use UpdateArticle.as_view()"""
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
def delete_article(request: HttpRequest, pk):
    """Old function. Use DeleteArticle.as_view()"""
    current_user = get_user(request)
    article = Articke.objects.get(id=pk)
    if request.method == "POST":
        content = f"user: {current_user}, delete article: {article.title}, with content:{article.content[:50]}."
        DeleteHistory.objects.create(user=current_user, content=content, article=True)
        article.delete()
    return redirect("home")
#######################################################################################

