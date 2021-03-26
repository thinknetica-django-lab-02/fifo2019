from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from .utils import OverwriteStorage

from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="products")
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="Продавец", related_name="products")
    title = models.CharField(max_length=128, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    image = models.ImageField(storage=OverwriteStorage(), upload_to='products/%Y%m%d/',
                              null=True, blank=True, verbose_name="Изображение")
    short_desc = models.CharField(max_length=60, blank=True, verbose_name='Краткое описание товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    is_active = models.BooleanField(default=True, verbose_name='Товар активен')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Tag(models.Model):
    title = models.CharField(max_length=128, unique=True, verbose_name='Тег')
    product = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']

    def __str__(self):
        return self.title


class Category(MPTTModel):
    title = models.CharField(max_length=100, unique=True, verbose_name="Категория")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True, verbose_name='Описание категории')
    is_active = models.BooleanField(default=True, verbose_name='Категория активна')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Продавец")
    image = models.ImageField(storage=OverwriteStorage(), upload_to='seller/%Y%m%d/',
                              null=True, blank=True, verbose_name="Аватарка")

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ['id']

    def __str__(self):
        return self.user.username
