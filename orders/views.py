from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class OrderCreteView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        super().post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NX2kYLXH8JXaLOAqMQQeW1X',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse("orders:order_success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse("orders:order_canceled")}',
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form: OrderForm) -> HttpResponseRedirect:
        form.instance.initiator = self.request.user
        return super().form_valid(form)


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
