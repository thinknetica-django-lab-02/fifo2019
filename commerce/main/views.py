from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from main.models import Product


class Home(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная"
        context['turn_on_block'] = True
        return context


class ProductList(ListView):

    model = Product

    template_name = 'main/products.html'
    context_object_name = 'products'
    extra_context = {'title': 'Продукты'}


class ProductDetail(DetailView):

    model = Product

    template_name = 'main/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        return context

