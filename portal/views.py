from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

import login_app.views
from .models import *
import requests
# from https://pynative.com/parse-json-response-using-python-requests-library/ for HTTPError
from requests.exceptions import HTTPError


def home(request):
    # from https://stackoverflow.com/questions/14639106/how-can-i-retrieve-a-list-of-field-for-all-objects-in-django
    uva_students = list(Student.objects.all().values_list('student_email', flat=True))
    uva_advisors = list(Advisor.objects.all().values_list('advisor_email', flat=True))
    if request.user.is_authenticated:
        if request.user.email in uva_students:
            return HttpResponseRedirect(reverse('portal:student_dashboard'))
        if request.user.email in uva_advisors:
            return HttpResponseRedirect(reverse('portal:advisor_dashboard'))

    return render(request, 'pages/home.html', {"students": uva_students, "advisors": uva_advisors})


def student(request):
    uva_students = list(Student.objects.all().values_list('student_email', flat=True))
    if request.user.is_authenticated and request.user.email in uva_students:
        student_logged_in = Student.objects.get(student_email=request.user.email)
        return render(request, 'pages/student_dashboard.html', {"student": student_logged_in})

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        year = request.POST['year']
        newStudent = Student(student_first_name=first_name, student_last_name=last_name,
                             student_email=email,
                             year_in_school=year)
        newStudent.save()
        return HttpResponseRedirect(reverse('portal:student_dashboard'))

    return render(request, "pages/student_sign_up.html")


def student_dashboard(request):
    student_logged_in = Student.objects.get(student_email=request.user.email)
    return render(request, 'pages/student_dashboard.html', {"student": student_logged_in})


def advisor(request):
    uva_advisors = list(Advisor.objects.all().values_list('advisor_email', flat=True))
    if request.user.is_authenticated and request.user.email in uva_advisors:
        advisor = Advisor.objects.get(advisor_email=request.user.email)
        return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor})

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        department = request.POST['department']
        # add some logic here for year
        newAdvisor = Advisor(advisor_first_name=first_name, advisor_last_name=last_name, advisor_email=email,
                             advisor_department=department)
        newAdvisor.save()
        return HttpResponseRedirect(reverse('portal:advisor_dashboard', args=(newAdvisor.id,)))

    return render(request, "pages/advisor_sign_up.html")


def get_departments():
    # r = requests.get(
    #     'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232')
    # # printing to file in your file explorer from https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    # departments = []
    # with open("class_lookup.txt", "a") as f:
    #     for key, value in r.json().items():
    #         if key == 'subjects':
    #             for v in value:
    #                 departments.append(v['descr'])
    departments = Department.objects.all()
    return departments


def student_class_lookup(request, student_id):
    student = Student.objects.get(pk=student_id)
    try:
        departments = get_departments()
        return render(request, 'pages/student_class_lookup.html',
                      {"student": student, "departments": departments, "error": ""})
    # from https://pynative.com/parse-json-response-using-python-requests-library/
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    return render(request, 'pages/student_class_lookup.html', {"student": student, "error": ""})


def class_results(request, student_id):
    print(request.user.email)
    test_student = Student.objects.get(student_email=request.user.email)
    print(test_student)
    student = Student.objects.get(pk=student_id)
    print(student)
    classes = Class.objects.filter(subject=request.POST['department']).order_by('catalog_nbr')
    return render(request, 'pages/class_results.html',
                  {"classes": classes, "student": student, "year": request.POST['year']})


def class_view(request, year):
    c = Class.objects.get(pk=request.POST['ClassPK'])
    baseURL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    url = baseURL + "&subject=" + c.subject + "&catalog_nbr=" + c.catalog_nbr + "&term=123" + year
    r = requests.get(url)
    classData = r.json()
    return render(request, 'pages/class_view.html', {"classData": classData, "class": c.subject + '-' + c.descr})


def advisor_dashboard(request, advisor_id):
    advisor = Advisor.objects.get(pk=advisor_id)
    return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor, })


def student_schedule(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'pages/student_schedule.html', {"student": student})
