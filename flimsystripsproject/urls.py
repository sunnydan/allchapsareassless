"""flimsystripsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from flimsystripsapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', views.register),
    path('accounts/profile', views.ProfileView.as_view()),
    path('accounts/logoutuser', views.logoutuser),
    path('updateuser', views.updateUser),
    path('cards', views.cards),
    path('newcard', views.newcard),
    path('likecard', views.likecard),
    path('unlikecard', views.unlikecard),
    path('deletecard', views.deletecard),
    path('decks', views.decks),
    path('newdeck', views.newdeck),
    path('updatedeck', views.updatedeck),
    path('addtodeck', views.addtodeck),
    path('addtagstodeck', views.addtagstodeck),
    path('removefromdeck', views.removefromdeck),
    path('deletedeck', views.deletedeck),
    path('displaydeck/<int:deckid>', views.displaydeck),
    path('', views.index),
    path('chat/', include('flimsystripsgame.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
