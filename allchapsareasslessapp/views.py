from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from allchapsareasslessapp.models import User, UserManager, Card, Tag, Deck
from allchapsareasslessapp.forms import RegistrationForm
from allchapsareasslessapp.util import handleAvatarUpdate
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    context = {
        "title": "Home",
    }
    return render(request, "index.html", context)


def cards(request):
    context = {
        "title": "Cards",
        "cards": Card.objects.all(),
    }
    return render(request, "cards/cards.html", context)


def newcard(request):
    if request.method == "POST" and request.user.is_authenticated:
        card = Card.objects.create_card(
            request.user, request.POST['svg'], request.POST['snapshot'])
        newtagstrings = request.POST['tags'].split(",")
        for newtagstring in newtagstrings:
            newtagstring = newtagstring.strip()
        for newtagstring in newtagstrings:
            try:
                tag = Tag.objects.get(name=newtagstring)
            except ObjectDoesNotExist:
                tag = Tag.objects.create_tag(newtagstring)
            if not card in tag.cards.all():
                tag.cards.add(card)
            tag.save()
        card.save()
    return redirect("/cards")


def likecard(request):
    card = Card.objects.get(id=request.POST["cardid"])
    if request.method == "POST" and request.user.is_authenticated and not request.user in card.likingUsers.all():
        card.likingUsers.add(request.user)
        card.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def unlikecard(request):
    card = Card.objects.get(id=request.POST["cardid"])
    if request.method == "POST" and request.user.is_authenticated and request.user in card.likingUsers.all():
        card.likingUsers.remove(request.user)
        card.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def deletecard(request):
    card = Card.objects.get(id=request.POST["cardid"])
    if request.method == "POST" and request.user.is_authenticated and card in request.user.cards.all():
        card.delete()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def newdeck(request):
    if request.method == "POST" and request.user.is_authenticated:
        deck = Deck.objects.create_deck(request.POST["name"], request.user)
        card = Card.objects.get(id=request.POST["cardid"])
        deck.cards.add(card)
        deck.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def updatedeck(request):
    deck = Deck.objects.get(id=request.POST["deckid"])
    if request.method == "POST" and request.user.is_authenticated and deck.author == request.user:
        newtagstrings = request.POST['tags'].split(",")
        for newtagstring in newtagstrings:
            newtagstring = newtagstring.strip()
        for newtagstring in newtagstrings:
            try:
                tag = Tag.objects.get(name=newtagstring)
            except ObjectDoesNotExist:
                tag = Tag.objects.create_tag(newtagstring)
            if not deck in tag.decks.all():
                tag.decks.add(deck)
            tag.save()
        deck.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def addtodeck(request):
    deck = Deck.objects.get(id=request.POST["deckid"])
    if request.method == "POST" and request.user.is_authenticated and deck.author == request.user:
        card = Card.objects.get(id=request.POST["cardid"])
        deck.cards.add(card)
        deck.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def removefromdeck(request):
    deck = Deck.objects.get(id=request.POST["deckid"])
    if request.method == "POST" and request.user.is_authenticated and deck.author == request.user:
        card = Card.objects.get(id=request.POST["cardid"])
        deck.cards.remove(card)
        deck.save()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


def deletedeck(request):
    deck = Deck.objects.get(id=request.POST["deckid"])
    if request.method == "POST" and request.user.is_authenticated and deck.author == request.user:
        deck.delete()
        return HttpResponse("success")
    else:
        return HttpResponse("failure")


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
            "cards": request.user.cards.all(),
        }
        return render(request, "profile.html", context)


def updateUser(request):
    if request.method == "POST":
        if request.POST.get("displayName") != "":
            request.user.displayName = request.POST.get("displayName")
            request.user.save()
        elif request.POST.get("avatar") != "":
            handleAvatarUpdate(request.FILES["avatar"], request.user)

    return redirect("/accounts/profile")
