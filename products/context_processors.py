from django.db.models import QuerySet
from django.http import HttpRequest

from products.models import Basket


def baskets(request: HttpRequest) -> dict[str, QuerySet[Basket] | list]:
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
