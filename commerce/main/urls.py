from django.urls import path

from .views import Home
from django.contrib.flatpages import views


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('contacts/', views.flatpage, {'url': '/contacts/'}, name='contacts'),
]
