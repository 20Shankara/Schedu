from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Student, Advisor
from .forms import StudentForm, AdvisorForm


# Create your views here.
def homepage(request):
    # from https://stackoverflow.com/questions/14639106/how-can-i-retrieve-a-list-of-field-for-all-objects-in-django 
    uva_students = list(Student.objects.all().values_list('student_email', flat=True))
    uva_advisors = list(Advisor.objects.all().values_list('advisor_email', flat=True))
    print(uva_students)
    print(uva_advisors)
    return render(request, 'pages/home.html', {"students": uva_students, "advisors": uva_advisors})


# def student_sign_up(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # print("-------")
#             # fn = form.cleaned_data.get('student_first_name')
#             # ln = form.cleaned_data.get('student_last_name')
#             # em = form.cleaned_data.get('student_email')
#             # print(fn)
#             # print(ln)
#             # print(em)
#             # print("-------")
#             return HttpResponseRedirect(reverse('portal:student_dashboard'), {"form": form})
#     else:
#         form = StudentForm()
#
#     return render(request, "pages/student_sign_up.html", {"form": form})

def student_sign_up(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            print("-------")
            fn = form.cleaned_data.get('student_first_name')
            ln = form.cleaned_data.get('student_last_name')
            em = form.cleaned_data.get('student_email')
            print(fn)
            print(ln)
            print(em)
            print("-------")
            return HttpResponseRedirect(reverse('portal:student_dashboard'), {"form": form})
    else:
        form = StudentForm()

    return render(request, "pages/student_sign_up.html", {"form": form})


# def student_dashboard(request):
#     students = Student.objects.all()
#     if 'student_first_name' in request.POST:
#         print("GOT A FIRST NAME")
#     print(students)
#     return render(request, 'pages/student_dashboard.html', {"Students": students})

def student_dashboard(request):
    students = Student.objects.all()  # fetch by email here, instead
    print(students)
    return render(request, 'pages/student_dashboard.html', {"Students": students})
