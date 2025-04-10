from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth import forms

# # Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    template_name = 'user/login.html'
    form = forms.AuthenticationForm()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            text = "Username or password is incorrect"
            messages.error(request=request, message=text)
            return render(request, template_name, {"form": form})
    return render(request, template_name, {"form": form})

def logout_view(request):
    logout(request)
    return redirect("user:login")
