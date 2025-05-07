from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import Http404

from cloudinary.utils import cloudinary_url

from comunication.models import DeleteHistory

from .models import Topic, Section, Code, Article, Links, Image, Note
from .forms import TopicForm, SectionForm, CodeForm, ArticleForm, LinksForm, ImageForm, NotesForm

# Create your views here.

class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    context_object_name = 'topics'

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().annotate(
            search_in_section = Count('section', filter=Q(section__title__icontains=self.search))
        ).filter(
            Q(name__icontains=self.search) |
            Q(short_description__icontains=self.search) |
            Q(search_in_section__gte=1)
        )

class TopicCreateView(LoginRequiredMixin, CreateView):
    form_class = TopicForm
    success_url = reverse_lazy('notebook:topic_list')

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('notebook.add_topic'):
            raise Http404
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
     
class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy('notebook:topic_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class TopicDetailCreateSectionView(LoginRequiredMixin, DetailView, CreateView):
    """ Show Topic detail, it is a section list(section_set).
        Create new section of instance topic"""
    model = Topic
    context_object_name = 'topic_object'
    form_class = SectionForm

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.filter(
            Q(topic=self.get_object()),
            Q(title__icontains=self.search) |
            Q(description__icontains=self.search),
        )
        return context
    
    def form_valid(self, form):
        form.instance.topic = self.get_object()
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('notebook:topic_detail',
                             kwargs={"pk": self.get_object().id})


class SectionDetailCreateView(LoginRequiredMixin, DetailView, CreateView):
    """ Base class of CodeSectionView, ArticleSectionView, LinksSectionView ,
        ImageSectionView. Have same logic for this classes"""
    model = Section
    context_object_name = 'section_object'
    
    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.section = self.get_object()
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class SectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Section

    def get_queryset(self):
        return super().get_queryset().filter(topic__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('notebook:topic_detail',
                             kwargs={"pk": self.get_object().topic.id})
    

class CodeSectionView(SectionDetailCreateView):
    form_class = CodeForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code_queryset'] = Code.objects.filter(
            Q(section=self.get_object()),
            Q(content__icontains=self.search),
        )
        return context
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_cod',
                             kwargs={"pk": self.get_object().id})

class CodeSectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Code

    def get_queryset(self):
        return super().get_queryset().filter(section__topic__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_cod',
                             kwargs={"pk": self.get_object().section.id})
    

class ArticleSectionView(SectionDetailCreateView):
    form_class = ArticleForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_queryset'] = Article.objects.filter(
            Q(section=self.get_object()),
            Q(content__icontains=self.search),
        )
        return context
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_articles',
                             kwargs={"pk": self.get_object().id})

class ArticleSectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Article

    def get_queryset(self):
        return super().get_queryset().filter(section__topic__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_articles',
                             kwargs={"pk": self.get_object().section.id})
    

class LinksSectionView(SectionDetailCreateView):
    form_class = LinksForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links_queryset'] = Links.objects.filter(
            Q(section=self.get_object()),
            Q(name__icontains=self.search)
        )
        return context
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_links',
                             kwargs={"pk": self.get_object().id})

class LinksSectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Links
    def get_queryset(self):
        return super().get_queryset().filter(section__topic__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_links',
                             kwargs={"pk": self.get_object().section.id})
    
    
class ImageSectionView(SectionDetailCreateView):
    form_class = ImageForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        image_queryset = Image.objects.filter(
            Q(section=self.get_object()),
            Q(image_title__icontains=self.search) |
            Q(image_description__icontains=self.search),
        )
        
        context['image_queryset'] = image_queryset
        return context
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_images',
                             kwargs={"pk": self.get_object().id})
    
    # def get_form(self, form_class = ...):
    #     form = ImageForm(self.request.POST, self.request.FILES)
    #     return form

class ImageSectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    def get_queryset(self):
        return super().get_queryset().filter(section__topic__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('notebook:show_images',
                             kwargs={"pk": self.get_object().section.id})
    

class BaseNoteView(View):
    """ Set the value used in child classes """
    model = Note
    def dispatch(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '')
        self.update_note = Note.objects.filter(
            id=kwargs.get('pk'),
            user=request.user
            ).first()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_note'] = self.update_note
        return context 
    
class NoteListView(BaseNoteView, ListView):
    context_object_name = 'notes'
    paginate_by = 5
    
    def get_paginate_by(self, queryset):
        if self.search != '':
            return
        return super().get_paginate_by(queryset)

    def get_queryset(self):
        
        queryset = super().get_queryset().filter(
            text__icontains=self.search,
            user=self.request.user,
        )
        return queryset

class NoteCreateView(BaseNoteView, CreateView):
    form_class = NotesForm
    success_url = reverse_lazy('notebook:notes_list_view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteView(LoginRequiredMixin, View):
    """ Depending on the method redirects the request """
    def get(self, request, *args, **kwargs):
        view = NoteListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = NoteCreateView.as_view()
        return view(request, *args, **kwargs)
    
class NoteUpdateView(LoginRequiredMixin, BaseNoteView, UpdateView):
    form_class = NotesForm
    template_name_suffix = '_list'
    success_url = reverse_lazy('notebook:notes_list_view')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(user=self.request.user)[:5]
        return context

class NotesDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('notebook:notes_list_view')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
