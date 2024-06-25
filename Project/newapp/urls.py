"""
URL configuration for newapp Application
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home)
]
