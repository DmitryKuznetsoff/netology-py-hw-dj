import random

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_favorites_retrieve_by_owner(favorites_factory, user_api_client, user):
    favorites = favorites_factory(min_amount=1, max_amount=1)[0]
    url = reverse('favorites-detail', args=[favorites.id])

    resp = user_api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert favorites.id == resp_json['id']


@pytest.mark.django_db
def test_favorites_retrieve_by_another_user(favorites_factory, another_user_api_client, user):
    favorites = favorites_factory(min_amount=1, max_amount=1)[0]
    url = reverse('favorites-detail', args=[favorites.id])

    resp = another_user_api_client.get(url)
    assert resp.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_favorites_list(favorites_factory, user_api_client):
    favorites_list = favorites_factory()
    url = reverse('favorites-list')

    resp = user_api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    expected_ids = {fav.id for fav in favorites_list}
    response_ids = {fav['id'] for fav in resp_json}
    assert response_ids == expected_ids


@pytest.mark.django_db
def test_favorites_create(favorites_factory, user_api_client, favorites_create_payload):
    url = reverse('favorites-list')

    resp = user_api_client.post(url, data=favorites_create_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED

    resp_json = resp.json()
    assert favorites_create_payload['product'] == resp_json['product']


@pytest.mark.django_db
def test_favorites_delete(favorites_factory, user_api_client):
    random_fav = random.choice(favorites_factory())
    url = reverse('favorites-detail', args=[random_fav.id])

    resp = user_api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT

    existing_ids = [product['id'] for product in user_api_client.get(reverse('favorites-list')).json()]
    assert random_fav.id not in existing_ids


@pytest.mark.django_db
def test_favorites_delete_by_another_user(favorites_factory, another_user_api_client):
    random_fav = random.choice(favorites_factory())
    url = reverse('favorites-detail', args=[random_fav.id])

    resp = another_user_api_client.delete(url)
    assert resp.status_code == HTTP_404_NOT_FOUND
