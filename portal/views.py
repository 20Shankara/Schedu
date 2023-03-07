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
    print(request.user)
    if request.user.is_authenticated:
        print("LOGGED IN")
        if request.user.email in uva_students:
            print("FOUND A STUDENT")
            student = Student.objects.get(student_email=request.user.email)
            print(student.id)
            return render(request, 'pages/student_dashboard.html', {"student": student})
        if request.user.email in uva_advisors:
            print("found an advisor")
            # eventually, mke this go to advisor dashboard
            return render(request, 'pages/home.html', {"students": uva_students, "advisors": uva_advisors})
    else:
        print("LOG IN WITH GOOGLE or SIGN UP")
        return render(request, 'pages/home.html', {"students": uva_students, "advisors": uva_advisors})


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
        newStudent = Student(student_first_name=first_name, student_last_name=last_name, student_email=email,
                             year_in_school=year)
        newStudent.save()
        print(newStudent.id)
        return HttpResponseRedirect(reverse('portal:student_dashboard', args=(newStudent.id,)))

    return render(request, "pages/student_sign_up.html")


def student_dashboard(request, student_id):
    student = Student.objects.get(pk=student_id)
    print(student)
    print("HIIIIIII")
    return render(request, 'pages/student_dashboard.html', {"student": student})
