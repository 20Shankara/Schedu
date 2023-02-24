from django.shortcuts import render

def login_dashboard(request):
    return render(request, 'main.html', {})