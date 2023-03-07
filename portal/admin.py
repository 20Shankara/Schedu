from django.contrib import admin
from .models import Student, Advisor


class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Student Information', {'fields': ['student_email', 'student_first_name', 'student_last_name', 'year_in_school']}),
    ]
    list_display = ('student_first_name', 'student_last_name', 'student_email')


admin.site.register(Student, StudentAdmin)
admin.site.register(Advisor)
