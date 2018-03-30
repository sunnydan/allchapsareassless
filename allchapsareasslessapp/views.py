from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")


def login(request):
    return render(request, "registration/login.html")


def register(request):
    context = {
        "form": UserCreationForm(),
    }
    return render(request, "registration/register.html", context)

def processregister(request):
    if request.method != "POST":
        return redirect("/")
    
