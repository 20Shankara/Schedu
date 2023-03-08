from django.contrib import admin
from .models import Student, Advisor


class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Student Information', {'fields': ['student_email', 'student_first_name', 'student_last_name', 'year_in_school']}),
    ]
    list_display = ('student_first_name', 'student_last_name', 'student_email', 'year_in_school')


class AdvisorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Advisor Information', {'fields': ['advisor_email', 'advisor_first_name', 'advisor_last_name', 'advisor_department']}),
    ]
    list_display = ('advisor_first_name', 'advisor_last_name', 'advisor_email', 'advisor_department')


admin.site.register(Student, StudentAdmin)
admin.site.register(Advisor, AdvisorAdmin)
