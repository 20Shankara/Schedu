import datetime
import json

import requests
from django.contrib import messages
from django.contrib.auth import logout
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from https://pynative.com/parse-json-response-using-python-requests-library/ for HTTPError
from requests.exceptions import HTTPError
from .models import *


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


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('portal:home'))


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
    class_nbr = request.POST['course_num']
    if class_nbr != "":
        print("Class Number: " + class_nbr)
        classes = Class.objects.filter(subject=request.POST['department']).filter(catalog_nbr=class_nbr)
    else:
        classes = Class.objects.filter(subject=request.POST['department']).order_by('catalog_nbr')
    return render(request, 'pages/class_results.html',
                  {"classes": classes, "student": test_student, "year": request.POST['year']})


def class_view(request, year):
    c = Class.objects.get(pk=request.POST['ClassPK'])
    baseURL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    url = baseURL + "&subject=" + c.subject + "&catalog_nbr=" + c.catalog_nbr + "&term=123" + year
    r = requests.get(url)
    classData = r.json()
    # logic here to fix times to be able to see in class view page - json will have long times like 15.30.00.00000
    for d in classData:
        for m in d['meetings']:
            if m['start_time'] != '':
                st_time = m['start_time'][0:5]
                en_time = m['end_time'][0:5]
                time_format = '%H.%M'  # The format
                st_time_str = datetime.datetime.strptime(st_time, time_format)
                st_time_str_2 = st_time_str.strftime("%I.%M %p")
                st_time_str_2 = st_time_str_2.replace(".", ":")
                en_time_str = datetime.datetime.strptime(en_time, time_format)
                en_time_str_2 = en_time_str.strftime("%I.%M %p")
                en_time_str_2 = en_time_str_2.replace(".", ":")
                m['start_time'] = st_time_str_2
                m['end_time'] = en_time_str_2
    return render(request, 'pages/class_view.html',
                  {"classData": classData, "class": c.subject + '-' + c.descr, "year": year})


def student_schedule(request):
    student_logged_in = Student.objects.get(student_email=request.user.email)
    schedule = []
    print(student_logged_in.schedule)
    if student_logged_in.schedule is None or len(student_logged_in.schedule.classes) == 0:
        return render(request, 'pages/student_schedule.html', {"schedule": "empty"})
    else:
        for item in student_logged_in.schedule.classes:
            curClass = ClassSection.objects.get(pk=item)
            schedule.append(curClass)
        schedule = serializers.serialize('json', schedule)
        data = json.loads(schedule)
        for d in data:
            if d['fields']['start_time'] != '':
                st_time = d['fields']['start_time'][0:5]
                en_time = d['fields']['end_time'][0:5]
                time_format = '%H.%M'  # The format
                st_time_str = datetime.datetime.strptime(st_time, time_format)
                st_time_str_2 = st_time_str.strftime("%I.%M %p")
                st_time_str_2 = st_time_str_2.replace(".", ":")
                en_time_str = datetime.datetime.strptime(en_time, time_format)
                en_time_str_2 = en_time_str.strftime("%I.%M %p")
                en_time_str_2 = en_time_str_2.replace(".", ":")
                d['fields']['start_time'] = st_time_str_2
                d['fields']['end_time'] = en_time_str_2
        return render(request, 'pages/student_schedule.html', {"schedule": data})


def student_schedule_warning(request):
    student_logged_in = Student.objects.get(student_email=request.user.email)
    schedule = []
    print(student_logged_in.schedule)
    # this if statement shouldn't be necessary...since no conflict will arise if schedule is empty
    if len(student_logged_in.schedule.classes) == 0:
        return render(request, 'pages/student_schedule.html', {"schedule": "empty"})
    else:
        for item in student_logged_in.schedule.classes:
            curClass = ClassSection.objects.get(pk=item)
            schedule.append(curClass)
        schedule = serializers.serialize('json', schedule)
        data = json.loads(schedule)
        for d in data:
            if d['fields']['start_time'] != '':
                st_time = d['fields']['start_time'][0:5]
                en_time = d['fields']['end_time'][0:5]
                time_format = '%H.%M'  # The format
                st_time_str = datetime.datetime.strptime(st_time, time_format)
                st_time_str_2 = st_time_str.strftime("%I.%M %p")
                st_time_str_2 = st_time_str_2.replace(".", ":")
                en_time_str = datetime.datetime.strptime(en_time, time_format)
                en_time_str_2 = en_time_str.strftime("%I.%M %p")
                en_time_str_2 = en_time_str_2.replace(".", ":")
                d['fields']['start_time'] = st_time_str_2
                d['fields']['end_time'] = en_time_str_2
        return render(request, 'pages/student_schedule_conflict.html', {"schedule": data})


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


def checkForConflicts(student_user, meetings):
    schedule = []
    if student_user.schedule is None:
        return False
    for item in student_user.schedule.classes:
        curClass = ClassSection.objects.get(pk=item)
        schedule.append(curClass)
    schedule = serializers.serialize('json', schedule)
    data = json.loads(schedule)
    print(data)
    # in case where there is no class in schedule, automatically, no conflict
    if not data:
        print("No conflict")
        return False
    else:
        print("--------PROPOSED CLASS--------")
        print(meetings['days'])
        print(meetings['start_time'])
        print(meetings['end_time'])
        print("-------------------")
        for c in data:
            if c['fields']['days'] == meetings['days']:
                print("SAME DAY")
                if c['fields']['start_time'] <= meetings['start_time'] <= c['fields']['end_time']:
                    print("Conflict with Start Time")
                    return True
                elif c['fields']['start_time'] <= meetings['end_time'] <= c['fields']['end_time']:
                    print("Conflict with End Time")
                    return True
            # print("-------------------")
            # print(c['fields']['days'])
            # print(c['fields']['start_time'])
            # print(c['fields']['end_time'])
            # print("-------------------")
        print("No conflict")
        return False


def add_to_schedule(request, year):
    class_nbr = (request.POST['class_number'])
    base_URL = baseURL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    url = base_URL + "&term=123" + year + "&class_nbr=" + class_nbr
    r = requests.get(url)
    r = r.json()[0]
    meetings = r['meetings'][0]
    student_logged_in = Student.objects.get(student_email=request.user.email)

    # check for class conflict
    conflict = checkForConflicts(student_logged_in, meetings)
    print(conflict)

    c = None
    if not ClassSection.objects.filter(class_nbr=r['class_nbr'], season=year).exists():
        # Logic for correcting start time and end time
        # st_time = meetings['start_time'][0:5]
        # en_time = meetings['end_time'][0:5]
        # time_format = '%H.%M'  # The format
        # st_time_str = datetime.datetime.strptime(st_time, time_format)
        # st_time_str_2 = st_time_str.strftime("%I.%M %p")
        # st_time_str_2 = st_time_str_2.replace(".", ":")
        # en_time_str = datetime.datetime.strptime(en_time, time_format)
        # en_time_str_2 = en_time_str.strftime("%I.%M %p")
        # en_time_str_2 = en_time_str_2.replace(".", ":")
        c = ClassSection(
            class_nbr=r['class_nbr'],
            class_section=r['class_section'],
            class_capacity=r['class_capacity'],
            enrollment_total=r['enrollment_total'],
            enrollment_available=r['enrollment_available'],
            units=r['units'],
            days=meetings['days'],
            # start_time=st_time_str_2,
            # end_time=en_time_str_2,
            start_time=meetings['start_time'],
            end_time=meetings['end_time'],
            instructor=meetings['instructor'],
            facility_descr=meetings['facility_descr'],
            catalog_nbr=r['catalog_nbr'],
            season=year,
            subject=r['subject'],
            subject_descr=r['subject_descr'],
            descr=r['descr'],
            section_type=r['section_type']
        )
        c.save()
    else:
        c = ClassSection.objects.get(class_nbr=class_nbr, season=year)

    # Check if student has a schedule
    schedule = None
    if student_logged_in.schedule is None:
        schedule = Schedule(season=year, classes=[])
        schedule.save()
        student_logged_in.schedule = schedule
        student_logged_in.save()
    else:
        schedule = student_logged_in.schedule

    if (not str(c.pk) in schedule.classes) and (not conflict) and (schedule.credit_count() + int(c.units[0]) <= 12):
        print("no conflicts with adding this class")
        schedule.classes.append(c.pk)
        schedule.save()
        cart = student_logged_in.shopping_cart
        print(cart.classes)
        cart.classes.remove(str(c.pk))
        cart.save()
        messages.success(request, "Class added to schedule.")
        return HttpResponseRedirect('/student_schedule')
    elif conflict:
        # todo: could try form.cleaned_data to access their decision before this method
        print("todo: remove this...time conflict")
        # this line below is key because it removes all messages, or else you will get long list that grows
        list(messages.get_messages(request))
        messages.warning(request, "Cannot add this class since you already have a class in your schedule at that time.")
        return HttpResponseRedirect(reverse('portal:student_schedule_conflict'))
    elif schedule.credit_count() + int(c.units[0]) > 12:
        # todo: could try form.cleaned_data to access their decision before this method
        print("todo: remove this...credits conflict")
        # this line below is key because it removes all messages, or else you will get long list that grows
        list(messages.get_messages(request))
        messages.warning(request, "Cannot add this class as you have already reached term credits limit.")
        return HttpResponseRedirect(reverse('portal:student_schedule_conflict'))


def add_class(request, year):
    class_nbr = (request.POST['Class_nbr'])
    base_URL = baseURL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    url = base_URL + "&term=123" + year + "&class_nbr=" + class_nbr
    r = requests.get(url)
    r = r.json()[0]
    meetings = r['meetings'][0]
    student_logged_in = Student.objects.get(student_email=request.user.email)

    c = None
    if not ClassSection.objects.filter(class_nbr=r['class_nbr'], season=year).exists():
        # Logic for correcting start time and end time
        # st_time = meetings['start_time'][0:5]
        # en_time = meetings['end_time'][0:5]
        # time_format = '%H.%M'  # The format
        # st_time_str = datetime.datetime.strptime(st_time, time_format)
        # st_time_str_2 = st_time_str.strftime("%I.%M %p")
        # st_time_str_2 = st_time_str_2.replace(".", ":")
        # en_time_str = datetime.datetime.strptime(en_time, time_format)
        # en_time_str_2 = en_time_str.strftime("%I.%M %p")
        # en_time_str_2 = en_time_str_2.replace(".", ":")
        c = ClassSection(
            class_nbr=r['class_nbr'],
            class_section=r['class_section'],
            class_capacity=r['class_capacity'],
            enrollment_total=r['enrollment_total'],
            enrollment_available=r['enrollment_available'],
            units=r['units'],
            days=meetings['days'],
            # start_time=st_time_str_2,
            # end_time=en_time_str_2,
            start_time=meetings['start_time'],
            end_time=meetings['end_time'],
            instructor=meetings['instructor'],
            facility_descr=meetings['facility_descr'],
            catalog_nbr=r['catalog_nbr'],
            season=year,
            subject=r['subject'],
            subject_descr=r['subject_descr'],
            descr=r['descr'],
            section_type=r['section_type']
        )
        c.save()
    else:
        c = ClassSection.objects.get(class_nbr=class_nbr, season=year)
    # Check if student has a shopping Cart
    shopping_cart = None
    if student_logged_in.shopping_cart is None:
        shopping_cart = ShoppingCart(season=year, classes=[])
        shopping_cart.save()
        student_logged_in.shopping_cart = shopping_cart
        student_logged_in.save()
    else:
        shopping_cart = student_logged_in.shopping_cart

    if not str(c.pk) in shopping_cart.classes:
        shopping_cart.classes.append(c.pk)
        shopping_cart.save()

    # this line below is key because it removes all messages, or else you will get long list that grows
    list(messages.get_messages(request))
    messages.success(request, "Class added to shopping cart.")
    return HttpResponseRedirect('/student_shopping_cart')


def remove_class(request):
    # TODO: have popup here to make sure they want to remove
    print(request.POST['class_pk'])
    student_logged_in = Student.objects.get(student_email=request.user.email)
    print(student_logged_in)
    student_logged_in.schedule.classes.remove(request.POST['class_pk'])
    student_logged_in.schedule.save()
    return HttpResponseRedirect(reverse('portal:home'))


def remove_from_shopping(request):
    # TODO: have popup here to make sure they want to remove
    print(request.POST['class_pk'])
    student_logged_in = Student.objects.get(student_email=request.user.email)
    print(student_logged_in)
    student_logged_in.shopping_cart.classes.remove(request.POST['class_pk'])
    student_logged_in.shopping_cart.save()
    return HttpResponseRedirect(reverse('portal:student_shopping_cart'))


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
    student_advisee = Student.objects.get(student_email=request.POST['advisee_email'])
    return render(request, 'pages/student_profile.html', {"student": student_advisee})


def advisor_schedule_view(request):
    print((request.POST['student_email']))
    student_advisee = Student.objects.get(student_email=request.POST['student_email'])
    schedule = []
    if student_advisee.schedule is None:
        return render(request, 'pages/advisor_schedule_view.html', {"schedule": {}})
    else:
        for item in student_advisee.schedule.classes:
            curClass = ClassSection.objects.get(pk=item)
            schedule.append(curClass)
        schedule = serializers.serialize('json', schedule)
        data = json.loads(schedule)
        return render(request, 'pages/advisor_schedule_view.html', {"schedule": data, "advisee": student_advisee})


def student_shopping_cart(request):
    student_logged_in = Student.objects.get(student_email=request.user.email)
    shopping_cart = []
    print(student_logged_in.shopping_cart)
    if (student_logged_in.shopping_cart is None) or (len(student_logged_in.shopping_cart.classes) == 0):
        return render(request, 'pages/student_shopping_cart.html', {"shopping_cart": "empty"})
    else:
        for item in student_logged_in.shopping_cart.classes:
            curClass = ClassSection.objects.get(pk=item)
            shopping_cart.append(curClass)
        shopping_cart = serializers.serialize('json', shopping_cart)
        data = json.loads(shopping_cart)
        for d in data:
            if d['fields']['start_time'] != '':
                st_time = d['fields']['start_time'][0:5]
                en_time = d['fields']['end_time'][0:5]
                time_format = '%H.%M'  # The format
                st_time_str = datetime.datetime.strptime(st_time, time_format)
                st_time_str_2 = st_time_str.strftime("%I.%M %p")
                st_time_str_2 = st_time_str_2.replace(".", ":")
                en_time_str = datetime.datetime.strptime(en_time, time_format)
                en_time_str_2 = en_time_str.strftime("%I.%M %p")
                en_time_str_2 = en_time_str_2.replace(".", ":")
                d['fields']['start_time'] = st_time_str_2
                d['fields']['end_time'] = en_time_str_2
        return render(request, 'pages/student_shopping_cart.html', {"shopping_cart": data})
