from http import HTTPStatus

from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductsCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()

    def test_list(self) -> None:
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self) -> None:
        category = ProductsCategory.objects.first()
        path = reverse('products:category', args=(category.id,))
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_tests(self, response: TemplateResponse) -> None:
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
