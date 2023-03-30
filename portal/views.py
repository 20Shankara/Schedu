from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

import login_app.views
from .models import Student, Advisor
import requests
# from https://pynative.com/parse-json-response-using-python-requests-library/ for HTTPError
from requests.exceptions import HTTPError


# def home(request):
#     return render(request, 'pages/home.html', )


def home(request):
    # from https://stackoverflow.com/questions/14639106/how-can-i-retrieve-a-list-of-field-for-all-objects-in-django
    uva_students = list(Student.objects.all().values_list('student_email', flat=True))
    uva_advisors = list(Advisor.objects.all().values_list('advisor_email', flat=True))
    if request.user.is_authenticated:
        if request.user.email in uva_students:
            student = Student.objects.get(student_email=request.user.email)
            return render(request, 'pages/student_dashboard.html', {"student": student})
        if request.user.email in uva_advisors:
            advisor = Advisor.objects.get(advisor_email=request.user.email)
            return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor})

    return render(request, 'pages/home.html', {"students": uva_students, "advisors": uva_advisors})


def student(request):
    uva_students = list(Student.objects.all().values_list('student_email', flat=True))
    if request.user.is_authenticated and request.user.email in uva_students:
        student = Student.objects.get(student_email=request.user.email)
        return render(request, 'pages/student_dashboard.html', {"student": student})

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        year = request.POST['year']
        # add some logic here for year
        newStudent = Student(student_first_name=first_name, student_last_name=last_name,
                             student_email=email,
                             year_in_school=year)
        newStudent.save()
        return HttpResponseRedirect(reverse('portal:student_dashboard', args=(newStudent.id,)))

    return render(request, "pages/student_sign_up.html")


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


def student_dashboard(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'pages/student_dashboard.html', {"student": student})


def get_departments():
    r = requests.get(
        'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232')
    # printing to file in your file explorer from https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    departments = []
    with open("class_lookup.txt", "a") as f:
        for key, value in r.json().items():
            if key == 'subjects':
                for v in value:
                    departments.append(v['descr'])
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
    # could pass as list of customized strings worse come worse
    # probably just get classes in as models
    try:
        student = Student.objects.get(pk=student_id)
        # TODO: take student_id out of parameters and just use request.user.id
        semester = request.POST['year']
        department = request.POST['department']
        course_number = request.POST['course_number']
        instructor_name = request.POST['instructor_name']

        term = '8' if semester[0:1] == 'f' else '2'
        year = semester[1:3]

        days = "".join(request.POST.getlist('days[]'))
        course_days = days
        enrl_stat = request.POST.get('enrl_stat', 'default')  # set default value if not open

        # https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=CS&page=1
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
        url = url + '&term=1' + year + term + '&subject=' + department
        # append course_number/ professor if inputted
        if course_number:
            url = url + '&class_nbr=' + course_number
        if instructor_name:
            url = url + '&instructor_name=' + instructor_name

        if len(days) != 0:
            url = url + '&days=' + days
        if enrl_stat == "O":
            url = url + '&enrl_stat=' + enrl_stat
        print(url)

        # looks like len(json) will be 0 if page has nothing, so that is way to tell in loop of all pages
        class_dictionary = {}
        open('department_classes2.txt', 'w').close()
        with open("department_classes2.txt", "a") as f:
            page_num = 1
            r = requests.get(url + '&page=' + str(page_num))
            classes = r.json()
            # COURSE NUMBER & PROFESSOR LOOKUP - redirect if incorrect course number

            # If user inputted incorrect fields then redirect back to lookup page:
            if ((len(classes) == 0) and course_number) or ((len(classes) == 0) and instructor_name):
                departments = get_departments()

                # NEED TO CHANGE ERROR MESSAGE BASED ON INPUT
                return render(request, 'pages/student_class_lookup.html',
                              {"student": student, "error": "Incorrect input", "departments": departments})

            while len(classes) != 0:
                for c in classes:
                    # print(c, file=f) # can uncomment this to see whole json output
                    professors = []
                    times = []
                    # days = []
                    locations = []
                    for prof in c['instructors']:
                        professors.append(prof['name'])
                    for info in c['meetings']:
                        professor = info['instructor']
                        times.append(info['start_time'])
                        # days.append(info['days'])
                        days = info['days']
                        locations.append(info['facility_descr'])
                    a_class = {
                        'title': c['descr'],
                        'id': c['crse_id'],
                        'number': c['catalog_nbr'],
                        'type': c['section_type'],
                        'professor': professors,
                        'class_capacity': c['class_capacity'],
                        'enrollment_available': c['enrollment_available'],
                        'status': c['enrl_stat_descr'],
                        'times': times,
                        'days': days,
                        'classroom': locations,
                    }
                    # if c['descr'] in class_dictionary: # needs to be course_id
                    #     class_dictionary[c['descr']].append(a_class)
                    # else:
                    #     class_dictionary[c['descr']] = []
                    #     class_dictionary[c['descr']].append(a_class)
                    # print(c["descr"])
                    # print(days)
                    # print(course_days)
                    # print(course_days == days)

                    if (days == course_days) & (course_days != ""):
                        if (c['catalog_nbr'] + " - " + c['descr']) in class_dictionary:  # needs to be course_id
                            class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])].append(a_class)
                        else:
                            class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])] = []
                            class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])].append(a_class)
                    # here we want all open discussions added even if days are specified
                    # discussion days won't match lecture requirements, but they still must see
                    if (a_class['type'] == "Discussion") & (course_days != ""):
                        # well, only want to add open discussion if there is open lecture
                        # only this if because it must already have lecture in there, so already an entry = shortcut
                        if (c['catalog_nbr'] + " - " + c['descr']) in class_dictionary:  # needs to be course_id
                            class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])].append(a_class)
                    # ----------------------------------------------------------------------------
                    # ----------------------------------------------------------------------------
                    # if course_days == "":
                    #     if (c['catalog_nbr'] + " - " + c['descr']) in class_dictionary:  # needs to be course_id
                    #         class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])].append(a_class)
                    #     elif (a_class['type'] == "Lecture") | (a_class['type'] == "SEM"):
                    #         class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])] = []
                    #         class_dictionary[(c['catalog_nbr'] + " - " + c['descr'])].append(a_class)
                    if course_days == "":
                        if a_class['number'] in class_dictionary:  # needs to be course_id
                            if (a_class['type'] == "Lecture") | (a_class['type'] == "SEM") | (a_class['type'] == "IND"):
                                class_dictionary[a_class['number']]["Lectures"].append(a_class)
                            elif a_class['type'] == "Discussion":
                                class_dictionary[a_class['number']]["Discussions"].append(a_class)
                        elif (a_class['type'] == "Lecture") | (a_class['type'] == "SEM") | (a_class['type'] == "IND"):
                            class_dictionary[a_class['number']] = {
                                "Course_Name": a_class['title'],
                                "Lectures": [],
                                "Discussions": []
                            }
                            class_dictionary[a_class['number']]["Lectures"].append(a_class)
                    # ----------------------------------------------------------------------------
                    # ----------------------------------------------------------------------------
                page_num += 1
                classes = requests.get(url + '&page=' + str(page_num)).json()
            print(class_dictionary, file=f)  # uncomment this to see what is added to dictionary for each class
        # print(class_set) # all unique names
        return render(request, 'pages/class_results.html',
                      {"student": student, "semester": semester, "department": department, "classes": class_dictionary})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return render(request, 'pages/student_class_lookup.html', {"student": student, "error":""})

def advisor_dashboard(request, advisor_id):
    advisor = Advisor.objects.get(pk=advisor_id)
    return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor})

def student_schedule(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'pages/student_schedule.html', {"student": student})
        return render(request, 'pages/student_class_lookup.html', {"student": student, "error": ""})
