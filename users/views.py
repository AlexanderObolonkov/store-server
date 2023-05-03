from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/login.html')


def registration(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/registration.html')
