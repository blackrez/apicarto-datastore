from django.conf.urls import include, url
from django.contrib import admin
from draw import views

urlpatterns = [
    url(r'^draw', views.store),
    url(r'^detail/(?P<reference>.+)', views.detail),
]