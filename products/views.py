from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import ProductsCategory, Product, Basket


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


@login_required
def basket_add(request: HttpRequest, product_id: int) -> HttpResponse:  # TODO: поменять на ManyToMany
    product = Product.objects.get(id=product_id)
    basket_item = Basket.objects.filter(user=request.user, product=product).first()

    if not basket_item:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket_item.quantity += 1
        basket_item.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request: HttpRequest, basket_id: int) -> HttpResponse:
    basket_item = Basket.objects.get(id=basket_id)
    basket_item.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
