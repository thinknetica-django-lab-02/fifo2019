from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from main.forms import *
from main.models import *


class Home(TemplateView):
    """Главная страница"""
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная"
        context['turn_on_block'] = True
        return context


class ProductList(ListView):
    """Список товаров"""

    model = Product
    template_name = 'main/products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Продукты'
        context['active_tag'] = 'all_goods'
        context['subsciber'] = Subsciber.objects.filter(user=self.request.user).first()
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

    def post(self, request, *args, **kwargs):
        if request.POST.get('mailing'):
            mailing = request.POST.get('mailing')
            if mailing == 'subscibe':
                Subsciber.objects.create(user=request.user)
            elif mailing == 'unsubscribe':
                subsciber = Subsciber.objects.filter(user_id=request.user.pk).first()
                if subsciber:
                    subsciber.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class ProductDetail(DetailView):
    """Карточка товара"""

    model = Product
    template_name = 'main/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    success_url = 'success_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product']
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = User
    form_class = UserForm
    template_name = 'main/auth/profile-update.html'
    success_url = '/accounts/profile/'
    login_url = reverse_lazy('account_login')

    def get_object(self, request):
        """Получение пользователя из request."""
        return request.user

    def get_context_data(self, **kwargs):
        """Добавление в контекст дополнительной формы"""
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        context['profile_form'] = ProfileFormSet(instance=self.get_object(kwargs['request']))
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
        Здесь происходит валидация основной формы и создание инстанса формы данным POST запроса
        """
        self.object = self.get_object(request)
        form = self.get_form()
        profile_form = ProfileFormSet(self.request.POST, self.request.FILES, instance=self.object)
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
        self.success_url = reverse('product', kwargs={'product_slug': instance.slug})
        return super(EditProduct, self).form_valid(form)


