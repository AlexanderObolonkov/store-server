from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from products.models import Product, ProductsCategory
from users.models import User


class ProductModelViewSetTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.token_admin = Token.objects.create(user=self.admin_user)
        self.category = ProductsCategory.objects.create(name='Test Category')
        self.product_data = {'name': 'Test Product', 'price': 9.99, 'category': self.category.id}
        self.product = Product.objects.create(name='Test Product', price=9.99, category=self.category)

    def test_list_products(self):
        url = reverse('api:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_product(self):
        url = reverse('api:product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(float(response.data['price']), self.product.price)

    def test_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_admin.key}')
        url = reverse('api:product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
