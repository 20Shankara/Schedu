from django.contrib import admin
from .models import Student, Advisor, Schedule


# class ScheduleInline(admin.TabularInline):
#     model = Schedule
#     extra = 0


class StudentAdmin(admin.ModelAdmin):
    # model = Student
    # inlines = [
    #     ScheduleInline
    # ]
    fieldsets = [
        ('Student Information',
         {'fields': ['student_email', 'student_first_name', 'student_last_name', 'year_in_school', 'advisor']}),
    ]
    list_display = ('student_first_name', 'student_last_name', 'student_email', 'year_in_school')


# https://stackoverflow.com/questions/20725426/django-displaying-one-to-many-relationship-in-the-admin-page
class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    exclude = ['schedule']


class AdvisorAdmin(admin.ModelAdmin):
    model = Advisor
    inlines = [
        StudentInline
    ]
    fieldsets = [
        ('Advisor Information',
         {'fields': ['advisor_email', 'advisor_first_name', 'advisor_last_name', 'advisor_department']}),
    ]
    list_display = ('advisor_first_name', 'advisor_last_name', 'advisor_email', 'advisor_department')


admin.site.register(Student, StudentAdmin)
admin.site.register(Advisor, AdvisorAdmin)
