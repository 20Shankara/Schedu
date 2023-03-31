from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    # -----------------------------------------------------------------------------------------------------
    #                                           STUDENTS
    # Student Sign-Up
    path('student_sign_up', views.student, name='student_link'),
    # Student Dashboard
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    # Class Lookup
    path('class_search', views.student_class_lookup, name='student_class_lookup'),
    # Class Lookup Results
    path('results', views.class_results, name='class_results'),
    # Class Sections
    path('<str:year>/class_view', views.class_view, name='class_view'),
    # Student's Schedule
    path('<int:student_id>/student_schedule/', views.student_schedule, name='student_schedule'),
    # -----------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    #                                           Advisors
    # Advisor Sign-Up
    path('advisor_sign_up', views.advisor, name='advisor_link'),
    # Advisor Dashboard
    path('advisor_dashboard', views.advisor_dashboard, name='advisor_dashboard'),
    # -----------------------------------------------------------------------------------------------------
]