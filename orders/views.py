from django.views.generic.base import TemplateView

# from django.views.generic.edit import CreateView


class OrderCreteView(TemplateView):
    template_name = 'orders/order-create.html'
    # form_class =
