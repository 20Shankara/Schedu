from django import forms
from .models import Student, Advisor


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['student_email']


class AdvisorForm(forms.ModelForm):
    class Meta:
        model = Advisor
        fields = '__all__'
