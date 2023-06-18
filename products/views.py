from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from products.models import ProductsCategory, Product, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Store'
        return context


def products(request: HttpRequest, category_id: int = 0, page_number: int = 1) -> HttpResponse:
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': ProductsCategory.objects.all(),
        'page_number': page_number,
        'selected_cat': category_id,
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
