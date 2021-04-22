from django.urls import path

from main.views import ProductDetail, Home, CreateProduct, EditProduct, \
    ProductList, ProfileUpdate
from django.contrib.flatpages import views
# from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', Home.as_view(), name='home'),
    # path('product/<slug:product_slug>/',
    #               cache_page(360)(ProductDetail.as_view()), name='product'),
    path('product/<slug:product_slug>/', ProductDetail.as_view(),
         name='product'),
    path('products/add/', CreateProduct.as_view(), name='create-product'),
    path('product/<slug:product_slug>/edit/', EditProduct.as_view(),
         name='edit-product'),
    path('products/', ProductList.as_view(), name='products'),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('contacts/', views.flatpage, {'url': '/contacts/'}, name='contacts'),
    path('accounts/profile/', ProfileUpdate.as_view(), name='profile-update'),
]
