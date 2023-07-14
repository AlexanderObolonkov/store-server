from django.urls import path

from orders.views import OrderCreteView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreteView.as_view(), name='order_create')
]
