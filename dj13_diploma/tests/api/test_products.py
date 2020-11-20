import random

from django.urls import reverse
import pytest
from rest_framework.status import HTTP_200_OK


@pytest.mark.django_db
def test_course_retrieve(api_client, product_factory):
    product = product_factory(min_amount=1, max_amount=1)[0]
    url = reverse('products-detail', args=[product.id])

    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert product.id == resp_json['id']


@pytest.mark.django_db
def test_course_list(api_client, product_factory):
    products_list = product_factory()
    url = reverse('products-list')

    resp = api_client.get(url)
    resp_json = resp.json()

    expected_ids = {product.id for product in products_list}
    response_ids = {product['id'] for product in resp_json}

    assert resp.status_code == HTTP_200_OK
    assert response_ids == expected_ids
