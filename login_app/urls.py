from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_dashboard, name="login_dashboard"),
]