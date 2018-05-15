from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from allchapsareasslessapp.models import User, UserManager
from allchapsareasslessapp.forms import RegistrationForm
from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.core.files.base import ContentFile
import os
import glob

AVATAR_IMAGE_SIZE = settings.AVATAR_IMAGE_SIZE


def index(request):
    context = {
        "title": "Home",
    }
    return render(request, "index.html", context)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/accounts/profile')
        else:
            return render(request, "registration/register.html", {"form": form, })
    else:
        form = RegistrationForm()
        return render(request, "registration/register.html", {"form": form, })


def logoutuser(request):
    return render(request, "registration/logout.html")


class ProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        context = {
            "title": "Profile",
        }
        return render(request, "profile.html", context)


def updateUser(request):
    if request.method == "POST":
        if request.POST.get("displayName") != "":
            request.user.displayName = request.POST.get("displayName")
            request.user.save()
        elif request.POST.get("avatar") != "":

            for filename in os.listdir(settings.MEDIA_ROOT+"/avatars"):
                if(filename.split(".")[0] == "avatar" + str(request.user.id)):
                    os.remove(os.path.join(
                        settings.MEDIA_ROOT+"\\avatars", filename))

                filetype = request.FILES['avatar'].name.split(".")[-1]
                if(filetype == "gif"):
                    request.FILES['avatar'].name = "avatar" + str(request.user.id) + ".gif"
                    request.user.avatar = request.FILES['avatar']
                    request.user.save()
                else:
                    image = Image.open(request.FILES['avatar'])
                    filetype = filetype.lower()

                    if(filetype.lower() == "jpg"):
                        filetype = "jpeg"

                    image = image.resize(
                        (AVATAR_IMAGE_SIZE, AVATAR_IMAGE_SIZE), Image.ANTIALIAS)

                    tempfile = BytesIO()
                    image.save(tempfile, filetype.lower())

                    image = InMemoryUploadedFile(
                        tempfile, None, "avatar" +
                        str(request.user.id) + "." + filetype, tempfile.__sizeof__, None, None)
                    request.user.avatar = image
                    request.user.save()
                    tempfile.close()

    return redirect("/accounts/profile")
