from django.http import HttpRequest, HttpResponse
from django.shortcuts import render



def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'products/index.html')


def products(request: HttpRequest) -> HttpResponse:
    return render(request, 'products/products.html')
