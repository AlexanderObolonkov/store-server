from django.db.models import QuerySet
from rest_framework import status
from rest_framework.permissions import (BasePermission, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product
from products.serializers import BasketSerializer, ProductSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self) -> QuerySet[Basket]:
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            product_id = request.data['product_id']
            product = Product.objects.filter(id=product_id).first()
            if not product:
                return Response(
                    {'product_id': 'There is no product with this ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            obj, is_created = Basket.create_or_update(product.id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'product_id': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
