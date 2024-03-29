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
    # Add Class to Shopping Cart
    path('<str:year>/add_class', views.add_class, name='add_class'),
    # Shopping Cart
    path('student_shopping_cart', views.student_shopping_cart, name='student_shopping_cart'),
    # Remove Class
    path('remove_class', views.remove_class, name='remove_class'),
    #Add Class to Schedule
    path('<str:year>/add_to_schedule', views.add_to_schedule, name='add_to_schedule'),
    #Remove Class to Schedule
    path('remove_from_shopping', views.remove_from_shopping, name='remove_from_shopping'),
    #Send Schedule to Advisor
    path('send_schedule', views.send_schedule, name='send_schedule'),

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
    path('view_schedule', views.advisor_schedule_view, name='advisor_schedule_view'),
    # Approve Student Schedule
    path('approve_schedule', views.approve_schedule, name='approve_schedule'),
    # Reject Student Schedule
    path('reject_schedule', views.reject_schedule, name='reject_schedule'),
    # -----------------------------------------------------------------------------------------------------
]