from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.homepage, name='home'),
    path('student', views.student_page, name='student_page'),
    path('advisor', views.advisor_page, name='advisor_page'),
]