from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.home, name='home'),
    path('student', views.student, name='student_link'),
    path('advisor', views.advisor, name='advisor_link'),
    path('<int:student_id>/student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('<int:advisor_id>/advisor_dashboard/', views.advisor_dashboard, name='advisor_dashboard'),
    path('<int:student_id>/student_class_lookup/', views.student_class_lookup, name='student_class_lookup'),
    path('<int:student_id>/class_results/', views.class_results, name='class_results'),
    path('<int:student_id>/student_schedule/', views.student_schedule, name='student_schedule'),
    path('<str:year>/class_view', views.class_view, name='class_view'),
    # might need to put filters as parameters in url here
    # path('<int:student_id>/<str:semester>/<str:department>/class_results/', views.class_results, name='class_results'),
]