from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.validators import validator_age
from django.core.mail import EmailMultiAlternatives
from allauth.account.signals import user_signed_up
from pytils.translit import slugify

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


class Subsciber(models.Model):
    """Подписка на рассылку"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subsciber", verbose_name="Пользователь")

    def __str__(self):
        return self.user.username


@receiver(pre_save, sender=Product)
def set_slug(sender, instance, *args, **kwargs):
    """Автозаполняет slug"""
    instance.slug = slugify(instance.title)


@receiver(user_signed_up)
def user_signed_up_(sender, request, user, **kwargs):
    subject, from_email, to_list = f"Пользователь {user}", 'paveldudkov003@gmail.com', [user.email]
    text_content = 'Благодарим Вас за интерес к нашему сайту!'
    html_content = '<p>Благодарим Вас за интерес к нашему сайту!</p>'
    sending_html_mail(subject, text_content, html_content, from_email, to_list)


def sending_html_mail(subject, text_content, html_content, from_email, to_list):
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Product)
def get_subsciber(sender, instance, created, **kwargs):
    if created:
        emails = [e.user.email for e in Subsciber.objects.all()]
        subject = f"Новый товар: {instance.title}"
        text_content = f"Появился новый товар {instance.title}. Все подробности по ссылке {instance.get_absolute_url}"
        html_content = f'''
            <h1>Появился новый товар {instance.title}</h1>
            <ul>
                <li>Описание: {instance.description}</li>
                <li>Цена: {instance.price}</li>
            </ul>
            Все подробности <a href="{instance.get_absolute_url()}">по ссылке</a>.
        '''
        from_email = 'paveldudkov003@gmail.com'
        sending_html_mail(subject, text_content, html_content, from_email, emails)
