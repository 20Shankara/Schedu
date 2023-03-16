from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Student, Advisor
import requests
# from https://pynative.com/parse-json-response-using-python-requests-library/ for HTTPError
from requests.exceptions import HTTPError


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
            print("FOUND AN ADVISOR")
            advisor = Advisor.objects.get(advisor_email=request.user.email)
            print(advisor.id)
            return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor})
    else:
        print("LOG IN WITH GOOGLE or SIGN UP")

    return render(request, 'pages/home.html', {"students": uva_students, "advisors": uva_advisors})


def student_sign_up(request):
    if request.method == "POST":
        id = request.user.id
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        year = request.POST['year']
        # change unique thing to id
        print('----------')
        print(first_name)
        print(last_name)
        print(email)
        print(year)
        print('----------')
        # add some logic here for year
        newStudent = Student(student_id=id, student_first_name=first_name, student_last_name=last_name,
                             student_email=email,
                             year_in_school=year)
        newStudent.save()
        # print(newStudent.id)
        return HttpResponseRedirect(reverse('portal:student_dashboard', args=(newStudent.id,)))

    return render(request, "pages/student_sign_up.html")


def student_dashboard(request, student_id):
    student = Student.objects.get(pk=student_id)
    print(student)
    print("HIIIIIII")
    return render(request, 'pages/student_dashboard.html', {"student": student})


def student_class_lookup(request, student_id):
    student = Student.objects.get(pk=student_id)
    print(student)
    try:
        # try passing year in from student_dashboard so on student dashboard you can select semester
        #      then edit this link accordingly.
        r = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232')
        # printing to file in your file explorer from https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
        departments = []
        # helper = []
        with open("class_lookup.txt", "a") as f:
            for key, value in r.json().items():
                if key == 'subjects':
                    # print(key, ":", value, file=f)
                    for v in value:
                        # dept = v['descr']
                        # x = dept.split(" - ", 1)
                        departments.append(v['descr'])
                        # helper.append(x)
            # print(departments, file=f)
            # for y in helper:
            #     print("<option value='" + y[1] + "'>" + y[1] + "</option>", file=f)
        if request.method == "POST":
            year = request.POST['year']
            department = request.POST['department']
            print(year)
            print(department)
            
            return HttpResponseRedirect(reverse('portal:class_results', args=(student_id, year, department,)))
        return render(request, 'pages/student_class_lookup.html', {"student": student, "departments": departments, "error":""})
    # from https://pynative.com/parse-json-response-using-python-requests-library/
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    return render(request, 'pages/student_class_lookup.html', {"student": student, "error":""})

def class_results(request, student_id):
    # could pass as list of customized strings worse come worse
    # probably just get classes in as models
    try: 
        student = Student.objects.get(pk=student_id)
        # TODO: take student_id out of parameters and just use request.user.id
        print('----------------------')
        print(request.POST['year'])
        semester = request.POST['year']
        department = request.POST['department']
        course_number = request.POST['course_number']
        instructor_name = request.POST['instructor_name']
        days = "".join(request.POST.getlist('days[]'))
        
        print('----------------------')
        print(student)
        term = semester[0:1]
        year = semester[1:3]
        print(term)
        print(year)
        print(course_number)
        print (instructor_name)
        print (days)
        
        # https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject=CS&page=1
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
        if term == 'f':
            term = '8'
            print(term)
        else:
            term = '2'
            print(term)
        url = url + '&term=1' + year + term + '&subject=' + department
        # append course_number/ professor if inputted
        if course_number != "":
            url = url + '&class_nbr=' + course_number
        if instructor_name != "":
            url = url + '&instructor_name=' + instructor_name
        if len(days) != 0:
            url = url + '&days=' + days
        print(url)
        # looks like len(json) will be 0 if page has nothing, so that is way to tell in loop of all pages
        class_dictionary = {}
        with open("department_classes2.txt", "a") as f:
            page_num = 1
            r = requests.get(url + '&page=' + str(page_num))
            classes = r.json()
            # COURSE NUMBER & PROFESSOR LOOKUP - redirect if incorrect course number
            if ((len(classes) == 0) & (course_number != '')) | ((len(classes) == 0) & (instructor_name != '')) | ((len(classes) == 0) & (days != '')): 
                r = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232')
                departments = []
                for key, value in r.json().items():
                    if key == 'subjects':
                        # print(key, ":", value, file=f)
                        for v in value:
                            # dept = v['descr']
                            # x = dept.split(" - ", 1)
                            departments.append(v['descr'])
                # NEED TO CHANGE ERROR MESSAGE BASED ON INPUT
                return render(request, 'pages/student_class_lookup.html', {"student": student, "error":"Incorrect input", "departments": departments})
            while len(classes) != 0:
                for c in classes:
                    # print(c, file=f) # can uncomment this to see whole json output
                    professors = []
                    times = []
                    days = []
                    locations = []
                    for prof in c['instructors']:
                        professors.append(prof['name'])
                    for info in c['meetings']:
                        professor = info['instructor']
                        times.append(info['start_time'])
                        days.append(info['days'])
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
                    if c['catalog_nbr'] in class_dictionary: # needs to be course_id
                        class_dictionary[c['catalog_nbr']].append(a_class)
                    else:
                        class_dictionary[c['catalog_nbr']] = []
                        class_dictionary[c['catalog_nbr']].append(a_class)
                page_num += 1
                classes = requests.get(url + '&page=' + str(page_num)).json()
            print(class_dictionary, file=f) # uncomment this to see what is added to dictionary for each class
        # print(class_set) # all unique names
        return render(request, 'pages/class_results.html',
                    {"student": student, "semester": semester, "department": department, "classes": class_dictionary})
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return render(request, 'pages/student_class_lookup.html', {"student": student, "error":""})
def advisor_sign_up(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        department = request.POST['department']
        print('----------')
        print(first_name)
        print(last_name)
        print(email)
        print(department)
        print('----------')
        # add some logic here for year
        newAdvisor = Advisor(advisor_first_name=first_name, advisor_last_name=last_name, advisor_email=email,
                             advisor_department=department)
        newAdvisor.save()
        print(newAdvisor.id)
        return HttpResponseRedirect(reverse('portal:advisor_dashboard', args=(newAdvisor.id,)))

    return render(request, "pages/advisor_sign_up.html")


def advisor_dashboard(request, advisor_id):
    advisor = Advisor.objects.get(pk=advisor_id)
    # print(advisor)
    print("HIIIIIII")
    return render(request, 'pages/advisor_dashboard.html', {"advisor": advisor})
