from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core import serializers
import json, ast

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
        # student_logged_in = Student.objects.get(student_email=request.user.email)
        # return render(request, 'pages/student_dashboard.html', {"student": student_logged_in})
        return HttpResponseRedirect(reverse('portal:student_dashboard'))

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


def get_departments():
    all_departments = Department.objects.all()
    return all_departments


def student_class_lookup(request):
    # TODO: fix this to be redirect
    student_logged_in = Student.objects.get(student_email=request.user.email)
    try:
        all_departments = get_departments()
        return render(request, 'pages/student_class_lookup.html',
                      {"student": student_logged_in, "departments": all_departments, "error": ""})
    # from https://pynative.com/parse-json-response-using-python-requests-library/
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    return render(request, 'pages/student_class_lookup.html', {"student": student_logged_in, "error": ""})


def class_results(request):
    test_student = Student.objects.get(student_email=request.user.email)
    classes = Class.objects.filter(subject=request.POST['department']).order_by('catalog_nbr')
    return render(request, 'pages/class_results.html',
                  {"classes": classes, "student": test_student, "year": request.POST['year']})


def class_view(request, year):
    c = Class.objects.get(pk=request.POST['ClassPK'])
    baseURL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    url = baseURL + "&subject=" + c.subject + "&catalog_nbr=" + c.catalog_nbr + "&term=123" + year
    r = requests.get(url)
    classData = r.json()
    return render(request, 'pages/class_view.html',
                  {"classData": classData, "class": c.subject + '-' + c.descr, "year": year})


def student_schedule(request):
    student_logged_in = Student.objects.get(student_email=request.user.email)
    schedule = []
    for item in student_logged_in.schedule.classes:
        curClass = ClassSection.objects.get(pk=item)
        schedule.append(curClass)
    schedule = serializers.serialize('json', schedule)
    data = json.loads(schedule)
    print(data)
    return render(request, 'pages/student_schedule.html', {"schedule": data})


def advisor(request):
    uva_advisors = list(Advisor.objects.all().values_list('advisor_email', flat=True))
    if request.user.is_authenticated and request.user.email in uva_advisors:
        return HttpResponseRedirect(reverse('portal:advisor_dashboard'))

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        department = request.POST['department']
        newAdvisor = Advisor(advisor_first_name=first_name, advisor_last_name=last_name, advisor_email=email,
                             advisor_department=department)
        newAdvisor.save()
        return HttpResponseRedirect(reverse('portal:advisor_dashboard'))

    return render(request, "pages/advisor_sign_up.html")


def advisor_dashboard(request):
    advisor_logged_in = Advisor.objects.get(advisor_email=request.user.email)
    return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor_logged_in})


def add_class(request, year):
    class_nbr = (request.POST['Class_nbr'])
    base_URL = baseURL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    url = baseURL + "&term=123" + year + "&class_nbr=" + class_nbr
    r = requests.get(url)
    r = r.json()[0]
    meetings = r['meetings'][0]
    c = None
    if not ClassSection.objects.filter(class_nbr=r['class_nbr'], season=year).exists():
        c = ClassSection(
            class_nbr=r['class_nbr'],
            class_section=r['class_section'],
            class_capacity=r['class_capacity'],
            enrollment_total=r['enrollment_total'],
            enrollment_available=r['enrollment_available'],
            units=r['units'],
            days=meetings['days'],
            start_time=meetings['start_time'],
            end_time=meetings['end_time'],
            instructor=meetings['instructor'],
            facility_descr=meetings['facility_descr'],
            catalog_nbr=r['catalog_nbr'],
            season=year,
        )
        c.save()
    else:
        c = ClassSection.objects.get(class_nbr=class_nbr, season=year)
    student = Student.objects.get(student_email=request.user.email)

    # Check if student has a schedule
    schedule = None
    if (student.schedule == None):
        schedule = Schedule(season=year, classes=[])
        schedule.save()
        student.schedule = schedule
        student.save()
    else:
        schedule = student.schedule

    if not str(c.pk) in schedule.classes:
        schedule.classes.append(c.pk)
        schedule.save()

    return HttpResponseRedirect('/student_schedule')


def manage_students(request):
    advisor_logged_in = Advisor.objects.get(advisor_email=request.user.email)
    advisees = list(Student.objects.filter(advisor=advisor_logged_in))
    if request.method == "POST":
        return HttpResponseRedirect(reverse('portal:student_profile'))
    # print(advisees)
    # for advisee in advisees:
    #     a_student = Student.objects.get(student_email=advisee.student_email)
    #     print(a_student.student_first_name)
    return render(request, 'pages/manage_students.html', {"advisees": advisees, "advisor": advisor_logged_in})


def student_profile(request):
    print((request.POST['advisee_email']))
    return render(request, 'pages/student_profile.html')
