from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    path('', views.home, name='home'),
    path('studentSignUp', views.student, name='student_link'),
    path('<int:student_id>/student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('<int:student_id>/student_class_lookup/', views.student_class_lookup, name='student_class_lookup'),
    # might need to put filters as parameters in url here
    # path('<int:student_id>/<str:semester>/<str:department>/class_results/', views.class_results, name='class_results'),
    path('<int:student_id>/class_results/', views.class_results, name='class_results'),
    path('<int:student_id>/class_results/', views.class_results, name='class_results'),
    path('advisorSignUp', views.advisor, name='advisor_link'),
    path('<int:advisor_id>/advisor_dashboard/', views.advisor_dashboard, name='advisor_dashboard'),
]