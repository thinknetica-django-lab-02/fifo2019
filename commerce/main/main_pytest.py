import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_list_view(client):
    response = client.get(reverse('products'))
    assert response.status_code == 200

