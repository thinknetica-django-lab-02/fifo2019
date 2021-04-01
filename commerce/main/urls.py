from django.urls import path

from main.views import *
from django.contrib.flatpages import views


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('product/<slug:product_slug>/', ProductDetail.as_view(), name='product'),
    path('products/', ProductList.as_view(), name='products'),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('contacts/', views.flatpage, {'url': '/contacts/'}, name='contacts'),
    path('accounts/profile/', ProfileUpdate.as_view(), name='profile-update'),
]
