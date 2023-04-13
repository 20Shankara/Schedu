from django.urls import path

from . import views

app_name = 'portal'
urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    path('logout', views.logout_user, name='logout'),
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
    path('student_schedule', views.student_schedule, name='student_schedule'),
    # Student's Schedule Conflict Page
    path('student_schedule_warning', views.student_schedule_warning, name='student_schedule_conflict'),
    # Add Class
    path('<str:year>/add_class', views.add_class, name='add_class'),
    # Remove Class
    path('remove_class', views.remove_class, name='remove_class'),

    # -----------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------
    #                                           Advisors
    # Advisor Sign-Up
    path('advisor_sign_up', views.advisor, name='advisor_link'),
    # Advisor Dashboard
    path('advisor_dashboard', views.advisor_dashboard, name='advisor_dashboard'),
    # Manage Students
    path('manage_students', views.manage_students, name='manage_students'),
    # Student Profile
    path('student_profile', views.student_profile, name='student_profile'),
    # Advisor Schedule View
    path('view_schedule', views.advisor_schedule_view, name='advisor_schedule_view')
    # -----------------------------------------------------------------------------------------------------
]