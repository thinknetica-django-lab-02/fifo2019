from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    def test_response_view(self):
        """
        Проверяет код ответ сервера, должен быть 200
        :return:
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class ProductListViewTests(TestCase):
    def test_response_view(self):
        """
        Проверяет код ответ сервера, должен быть 200
        :return:
        """
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)

