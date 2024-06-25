from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Redirects the User to the Home Screen"""
    # return HttpResponse("Hello World")
    return render(request, 'index.html')
