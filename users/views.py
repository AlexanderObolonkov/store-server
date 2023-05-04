from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from users.models import User
from users.forms import UserLoginForm


def login(request: HttpRequest) -> HttpResponse:
    context = {'form': UserLoginForm()}
    return render(request, 'users/login.html', context)


def registration(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/registration.html')
