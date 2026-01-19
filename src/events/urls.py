from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("events/search/", views.events_search, name='events_search'),
    path("events/create/", views.events_create, name='events_create'),
    path("accounts/create/", views.accounts_create, name='accounts_create'),
    path("accounts/login/", views.accounts_login, name='accounts_login'),
    path("accounts/logout/", views.accounts_logout, name='accounts_logout'),
]
