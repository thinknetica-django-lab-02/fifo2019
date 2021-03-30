from django.views.generic import TemplateView, ListView, DetailView

from main.models import Product, Tag


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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        context['active_tag'] = 'all_goods'
        context['tags'] = Tag.objects.all()

        if self.request.GET.get('tag'):
            tag_name = self.request.GET.get('tag')
            context['active_tag'] = tag_name

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('tag'):
            tag_name = self.request.GET.get('tag')

            if tag_name != 'all_goods':
                return queryset.filter(tags__title=tag_name)

        return queryset


class ProductDetail(DetailView):

    model = Product

    template_name = 'main/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        return context

