from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    # -----------------------------------------------------------------------------------------------------
    #                                           STUDENTS
    # Student Sign-Up
    path('sign_up', views.student, name='student_link'),
    # Student Dashboard
    path('dashboard', views.student_dashboard, name='student_dashboard'),
    # Class Lookup
    path('<int:student_id>/student_class_lookup/', views.student_class_lookup, name='student_class_lookup'),
    # Class Lookup Results
    path('<int:student_id>/class_results/', views.class_results, name='class_results'),
    # Class Sections
    path('<str:year>/class_view', views.class_view, name='class_view'),
    # Student's Schedule
    path('<int:student_id>/student_schedule/', views.student_schedule, name='student_schedule'),
    # -----------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    #                                           Advisors
    # Advisor Sign-Up
    path('advisor', views.advisor, name='advisor_link'),
    # Advisor Dashboard
    path('<int:advisor_id>/advisor_dashboard/', views.advisor_dashboard, name='advisor_dashboard'),
    # -----------------------------------------------------------------------------------------------------
]