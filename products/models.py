import stripe
from _decimal import Decimal
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_PRIVATE_KEY


class ProductsCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(ProductsCategory, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category}'

    def save(
            self, force_insert: bool = False, force_update: bool = False, using: bool = None, update_fields: bool = None
    ) -> None:
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super().save(force_insert, force_update, using, update_fields)

    def create_stripe_product_price(self) -> stripe.Price:
        kopecks_in_rubles = 100

        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * kopecks_in_rubles),
            currency='rub'
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self) -> Decimal:
        return sum(basket.sum() for basket in self)

    def total_quantity(self) -> int:
        return sum(basket.quantity for basket in self)

    def stripe_products(self) -> list[dict[str, int]]:
        line_items = [{'price': basket.product.stripe_product_price_id,
                       'quantity': basket.quantity}
                      for basket in self]
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self) -> Decimal:
        return self.product.price * self.quantity
