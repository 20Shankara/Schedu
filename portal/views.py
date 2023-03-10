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


def student_class_lookup(request, student_id):
    student = Student.objects.get(pk=student_id)
    print(student)
    try:
        # try passing year in from student_dashboard so on student dashboard you can select semester
        #      then edit this link accordingly.
        r = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1228')
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
        return render(request, 'pages/student_class_lookup.html', {"student": student, "departments": departments})
    # from https://pynative.com/parse-json-response-using-python-requests-library/
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    return render(request, 'pages/student_class_lookup.html', {"student": student})


def class_results(request, student_id, semester, department):
    student = Student.objects.get(pk=student_id)
    print(student)
    term = semester[0:1]
    year = semester[1:3]
    print(term)
    print(year)
    url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01'
    if term == 'f':
        term = '8'
        print(term)
    else:
        term = '2'
        print(term)
    url = url + '&term=1' + year + term + '&subject=' + department
    print(url)
    # looks like len(json) will be 0 if page has nothing, so that is way to tell in loop of all pages
    filter_results = []
    with open("department_classes.txt", "a") as d:
        page_num = 1
        r = requests.get(url + '&page=' + str(page_num))
        classes = r.json()
        while len(classes) != 0:
            for c in classes:
                for prof in c['instructors']:
                    # print(c['descr'] + ' - ' + c['section_type'] + "(" + prof['name'] + ")", file=d)
                    filter_results.append(c['descr'] + ' - ' + c['section_type'] + "(" + prof['name'] + ")")
            page_num += 1
            classes = requests.get(url + '&page=' + str(page_num)).json()
    return render(request, 'pages/class_results.html',
                  {"student": student, "semester": semester, "department": department, "classes": filter_results})


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
