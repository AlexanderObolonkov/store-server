from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from products.models import ProductsCategory, Product


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context)


def products(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductsCategory.objects.all()
    }
    return render(request, 'products/products.html', context)
