from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.validators import validator_age
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# Apscheduler
# import atexit
# from apscheduler.schedulers.background import BackgroundScheduler

from mptt.models import MPTTModel, TreeForeignKey

# from main.tasks import sending_html_mail_task


class Product(models.Model):

    """Модель товара."""

    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    seller = models.ForeignKey(
        'Seller', on_delete=models.SET_NULL,
        null=True, blank=True, related_name="products",
        verbose_name="Продавец"
    )
    tags = ArrayField(
        models.CharField(max_length=100, blank=True),
        default=list, verbose_name='Теги'
    )
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    image = models.ImageField(upload_to='products/', blank=True, null=True,
                              verbose_name="Изображение")
    short_desc = RichTextUploadingField()
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0,
                                verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(default=0,
                                           verbose_name='Количество на складе')
    discount = models.IntegerField(default=0, verbose_name='Скидка')
    is_active = models.BooleanField(default=True, verbose_name='Товар активен')
    views = models.IntegerField(default=0)

    class Meta:
        """Настройки для админ панели

        :param verbose_name: Название товара в ед. числе
        :type verbose_name: str
        :param verbose_name_plural: Название товара в мн. числе
        :type verbose_name: str
        :param ordering: Сортировка
        :type ordering: list
        """
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']

    def __str__(self) -> str:
        """Стоковое представлени

        :return: Возвращает название товара
        :rtype: str
        """
        return self.title

    def get_absolute_url(self) -> str:
        """Получает абсолютный путь

        :return: Возвращает url товара до представления
        :rtype: str
        """
        return reverse('product', kwargs={'product_slug': self.slug})


class ViewsProduct(models.Model):
    views = models.IntegerField(default=0)

    class Meta:
        managed = False


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/',
                              verbose_name="Изображение")
    product = models.ForeignKey('Product', on_delete=models.CASCADE,
                                related_name="gallery", verbose_name="Товар")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображений'
        ordering = ['id']

    def __str__(self) -> str:
        return self.image.url


class Category(MPTTModel):
    title = models.CharField(max_length=100, unique=True,
                             verbose_name="Категория")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    description = models.TextField(blank=True,
                                   verbose_name='Описание категории')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Категория активна')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('category', kwargs={'category_slug': self.slug})


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="Продавец")
    avatar = models.ImageField(upload_to='seller/', null=True, blank=True,
                               verbose_name="Аватарка")

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ['id']

    def __str__(self) -> str:
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="profile",
                                verbose_name="Пользователь")
    date_of_birth = models.DateField(validators=[validator_age], blank=True,
                                     null=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='profile/', null=True, blank=True,
                               verbose_name="Аватарка")

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['id']

    def __str__(self) -> str:
        return f"Профиль: {self.user.username}"

    @receiver(post_save, sender=User)
    def user_profile(sender, instance, created, **kwargs) -> None:
        if created:
            Profile.objects.create(user=instance)
            instance.groups.add(
                Group.objects.get_or_create(name='common users')[0])
        instance.profile.save()


class Subsciber(models.Model):
    """Подписка на рассылку"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="subsciber",
                                verbose_name="Пользователь")

    def __str__(self) -> str:
        return self.user.username


class SMSLog(models.Model):
    """Сгенерированные кода по смс"""
    code = models.IntegerField()
    response_server = models.CharField(max_length=200)

    def __str__(self) -> int:
        return self.code


@receiver(pre_save, sender=Product)
def set_slug(sender, instance, *args, **kwargs):
    """Автозаполняет slug"""
    instance.slug = slugify(instance.title)

# Apscheduler
# sched = BackgroundScheduler()
# sched.add_job(
#     sending_new_products, 'cron',
#     day_of_week='sun', hour=14, minute=00,
#     timezone='Europe/Moscow', start_date='2021-04-11'
# )
# sched.start()
# atexit.register(lambda: sched.shutdown())
