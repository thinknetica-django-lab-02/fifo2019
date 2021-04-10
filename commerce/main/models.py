from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.validators import validator_age
from django.core.mail import EmailMultiAlternatives, send_mail
from allauth.account.signals import user_signed_up

from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name="products", verbose_name="Продавец")
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Теги')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    short_desc = models.CharField(max_length=60, blank=True, verbose_name='Краткое описание товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    discount = models.IntegerField(default=0, verbose_name='Скидка')
    is_active = models.BooleanField(default=True, verbose_name='Товар активен')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="gallery", verbose_name="Товар")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображений'
        ordering = ['id']

    def __str__(self):
        return self.image


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Тег')

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Продавец")
    avatar = models.ImageField(upload_to='seller/', null=True, blank=True, verbose_name="Аватарка")

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ['id']

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Пользователь")
    date_of_birth = models.DateField(validators=[validator_age], blank=True, null=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='profile/', null=True, blank=True, verbose_name="Аватарка")

    class Meta:
        verbose_name = f'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['id']

    def __str__(self):
        return f"Профиль: {self.user.username}"

    @receiver(post_save, sender=User)
    def user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.groups.add(Group.objects.get_or_create(name='common users')[0])
        instance.profile.save()


@receiver(user_signed_up)
def user_signed_up_(sender, request, user, **kwargs):
    # subject, from_email, to = f"Успешная регистрация {user}", 'paveldudkov003@gmail.com', user.email
    # text_content = 'Благодарим Вас за регистрации на нашем сайте!'
    # html_content = '<p>Благодарим Вас за регистрации на нашем сайте!</p>'
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    send_mail(
        f'Успешная регистрация {user}',
        'Благодарим Вас за регистрацию.',
        'from@example.com',
        ['from@example.com'],
    )
