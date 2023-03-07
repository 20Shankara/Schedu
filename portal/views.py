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
#             print("-------")
#             fn = form.cleaned_data.get('student_first_name')
#             ln = form.cleaned_data.get('student_last_name')
#             yr = form.cleaned_data.get('year_in_school')
#             fn2 = request.POST['student_first_name']
#             ln2 = request.POST['student_last_name']
#             # newStudent = Student(student_first_name=fn2+'zzz', student_last_name=ln2+'zzz')
#             # newStudent.save()
#             print("-------")
#             return HttpResponseRedirect(reverse('portal:student_dashboard', {"form": form}))
#     else:
#         form = StudentForm()
#
#     return render(request, "pages/student_sign_up.html")

# def student_sign_up(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('portal:student_dashboard'))
#     else:
#         form = StudentForm()
#
#     return render(request, "pages/student_sign_up.html", {"form": form})

def student_sign_up(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        year = request.POST['year']
        print('----------')
        print(first_name)
        print(last_name)
        print(email)
        print(year)
        print('----------')
        # add some logic here for year
        newStudent = Student(student_first_name=first_name, student_last_name=last_name, student_email=email, year_in_school=year)
        newStudent.save()
        # this should be redirect...in dashboard can fetch all information by getting student profile based off email
        return render(request, 'pages/student_dashboard.html')

    return render(request, "pages/student_sign_up.html")


def student_dashboard(request):
    students = Student.objects.all()  # fetch by email here, instead
    print(students)
    return render(request, 'pages/student_dashboard.html', {"Students": students})
