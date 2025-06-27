from django.shortcuts import render
from .models import AboutMe, Projects, Education, Skills, Hobbies

# Create your views here.
def about(request):
    about = AboutMe.objects.first()


    projects = Projects.objects.all()
    education = Education.objects.first()
    skills = Skills.objects.first()
    hobbies = Hobbies.objects.first()

    context={
        'about': about,
        'projects': projects,
        'education': education,
        'skills': skills,
        'hobbies': hobbies,
    }
    return render(request=request, template_name='about/about_me.html', context=context)