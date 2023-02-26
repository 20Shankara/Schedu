from django.shortcuts import render


def login_dashboard(request):
    return render(request, 'main.html', {})

def student_homepage(request):
    return render(request, 'student_homepage.html', )


def advisor_homepage(request):
    return render(request, 'advisor_homepage.html', )