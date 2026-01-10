from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    # path("events/order/", views.order_events, name='order_events'),
]
