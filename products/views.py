from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from products.models import ProductsCategory, Product, Basket
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data()
        context['categories'] = ProductsCategory.objects.all()
        return context


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
