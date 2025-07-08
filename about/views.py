from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import AboutMe, Projects, Education, Skills, Hobbies, LanguageChoices

# Create your views here.
def about(request):
    language = request.GET.get('lang')
    if language == 'uk':
        about = get_object_or_404(AboutMe, language=LanguageChoices.UKRAINE)
    elif language == 'en':
        about = get_object_or_404(AboutMe, language=LanguageChoices.ENGLISH)
    else:
        about = get_object_or_404(AboutMe, language=LanguageChoices.ENGLISH)
    
    projects = Projects.objects.filter(about=about)
    education = Education.objects.filter(about=about).first()
    skills = Skills.objects.filter(about=about).first()
    hobbies = Hobbies.objects.filter(about=about).first()

    context={
        'about': about,
        'projects': projects,
        'education': education,
        'skills': skills,
        'hobbies': hobbies,
        'language': language
    }
    return render(request=request, template_name='about/about_me.html', context=context)

def about_en(request):
    about = AboutMe.objects.filter(language=LanguageChoices.UKRAINE).first()
    projects = Projects.objects.filter(about=about)
    education = Education.objects.get(about=about)
    skills = Skills.objects.get(about=about)
    hobbies = Hobbies.objects.get(about=about)

    context={
        'about': about,
        'projects': projects,
        'education': education,
        'skills': skills,
        'hobbies': hobbies,
    }
    return render(request=request, template_name='about/about_me.html', context=context)
