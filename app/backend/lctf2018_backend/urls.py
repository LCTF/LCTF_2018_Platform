"""lctf2018_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import backend.views

urlpatterns = [
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/login$', backend.views.login),
    url(r'^api/logout$', backend.views.logout),
    url(r'^api/register$', backend.views.register),
    url(r'^api/get_token$', backend.views.get_csrf_token),
    url(r'^api/get_all$', backend.views.get_all),
    url(r'^api/get_index$', backend.views.get_index),
    url(r'^api/submit$', backend.views.submit),
    url(r'^api/get_score$', backend.views.get_score),
    url(r'^api/scoreboard$', backend.views.scoreboard),
    url(r"^api/challenge_rank$", backend.views.challenge_rank),
    url(r'^api/team/(\d+)/$', backend.views.teaminfo),
]
