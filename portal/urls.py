from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.homepage, name='home'),
    path('studentSignUp', views.student_sign_up, name='student_link'),
    path('<int:student_id>/student_dashboard/', views.student_dashboard, name='student_dashboard'),
]