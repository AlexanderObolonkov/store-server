from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreteView,
                          OrderDetailView, OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-create/', OrderCreteView.as_view(), name='order_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]
