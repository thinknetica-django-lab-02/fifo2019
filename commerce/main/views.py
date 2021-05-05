from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms.forms import Form
from django.http import HttpResponseRedirect, HttpResponse
from django.http.request import HttpRequest
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, \
    UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from main.forms import UserForm, ProfileFormSet, ProductForm
from main.models import Product, Subsciber

from django.db.models import F
from django.core.cache import cache

from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector


class Home(TemplateView):
    """Главная страница"""
    template_name: str = "main/index.html"

    def get_context_data(
        self,
        **kwargs: dict
    ) -> dict:
        context: dict = super().get_context_data(**kwargs)
        context['title'] = "Главная"
        context['description'] = "Описание главной страницы для E-commerce"
        context['turn_on_block'] = True
        return context


class ProductList(ListView):
    """Список товаров"""

    model: Model = Product
    template_name: str = 'main/products.html'
    context_object_name: str = 'products'
    paginate_by: int = 9

    def get_context_data(
        self,
        **kwargs: dict
    ) -> dict:
        context: dict = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        context['description'] = "Описание страницы c товарами"
        context['active_tag'] = 'all_goods'
        context['subsciber'] = Subsciber.objects.filter(
                                   user__pk=self.request.user.pk
                               ).first()
        context['tags'] = set()
        for tag_list in Product.objects.values_list('tags'):
            if tag_list[0]:
                for tag in tag_list[0]:
                    context['tags'].add(tag)

        if self.request.GET.get('tag'):
            tag_name: str = self.request.GET.get('tag')
            context['active_tag'] = tag_name

        return context

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = super().get_queryset()

        if self.request.GET.get('tag'):
            tag_name: str = self.request.GET.get('tag')

            if tag_name != 'all_goods':
                return queryset.filter(tags__overlap=[tag_name])

        return queryset

    def post(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponseRedirect:
        if request.POST.get('mailing'):
            mailing: str = request.POST.get('mailing')
            if mailing == 'subscibe':
                Subsciber.objects.create(user=request.user)
            elif mailing == 'unsubscribe':
                subsciber = Subsciber.objects.filter(
                    user_id=request.user.pk).first()
                if subsciber:
                    subsciber.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class SearchProduct(ListView):
    """Поиск товара"""

    model = Product
    template_name = 'main/search.html'
    context_object_name = 'products'
    paginate_by: int = 9

    def get_context_data(self, **kwargs):
        context: dict = super().get_context_data(**kwargs)
        context['title'] = 'Результат поиска'

        if self.request.GET.get('q'):
            search_world = self.request.GET.get('q')
            context['title'] += f' "{search_world}"'
            context['search_world'] = search_world

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('q'):
            search_world = self.request.GET.get('q')

            return Product.objects.annotate(
                search=SearchVector('title', 'description'),
            ).filter(search=search_world)

        return queryset


class ProductDetail(DetailView):
    """Карточка товара"""

    model: Model = Product
    template_name: str = 'main/product.html'
    slug_url_kwarg: str = 'product_slug'
    context_object_name: str = 'product'
    success_url: str = 'success_url'

    def get_context_data(
        self,
        **kwargs: dict
    ) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        context['description'] = f"Описание страницы товара: {context['product']}"
        context['views'] = cache.get_or_set(f"view-{self.object.pk}",
                                            f"{self.object.views}", 60)
        return context

    def get(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        Product.objects.filter(slug=self.kwargs['product_slug'])\
                       .update(views=F('views') + 1)
        return super().get(request, *args, **kwargs)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model: Model = User
    form_class: Form = UserForm
    template_name: str = 'main/auth/profile-update.html'
    success_url: str = '/accounts/profile/'
    login_url = reverse_lazy('account_login')

    def get_object(self, request):
        """Получение пользователя из request."""
        return request.user

    def get_context_data(self, **kwargs):
        """Добавление в контекст дополнительной формы"""
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        context['profile_form'] = ProfileFormSet(
            instance=self.get_object(kwargs['request']))
        return context

    def get(self, request, *args, **kwargs):
        """Метод обрабатывающий GET запрос.
        Переопределяется только из-за self.get_object(request)
        """
        self.object = self.get_object(request)
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid_formset(self, form, formset):
        """Валидация вложенной формы и сохранение обеих форм."""
        if formset.is_valid():
            formset.save(commit=False)
            formset.save()
        else:
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """Метод обрабатывающий POST запрос.
        Здесь происходит валидация основной формы и создание инстанса формы
        данным POST запроса
        """
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormSet(self.request.POST, self.request.FILES,
                                      instance=self.object)
        if form.is_valid():
            return self.form_valid_formset(form, profile_form)
        else:
            return self.form_invalid(form)


class CreateProduct(LoginRequiredMixin, CreateView):
    """Создание товара"""
    model = Product
    form_class = ProductForm
    template_name = 'main/product-form.html'
    login_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление товара"
        context['mode'] = "create"
        return context


class EditProduct(LoginRequiredMixin, UpdateView):
    """Редактирование карточки продукта"""
    model = Product
    form_class = ProductForm
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    template_name = 'main/product-form.html'
    login_url = reverse_lazy('account_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование товара"
        context['mode'] = "edit"
        return context

    def form_valid(self, form):
        instance = form.save()
        self.success_url = reverse('product',
                                   kwargs={'product_slug': instance.slug})
        return super(EditProduct, self).form_valid(form)
