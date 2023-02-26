from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_dashboard, name="login_dashboard"),
    path('student', views.student_homepage, name='student_homepage'),
    path('advisor', views.advisor_homepage, name='advisor_homepage'),
]
