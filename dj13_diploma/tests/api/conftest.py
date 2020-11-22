from random import randint

import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='user', password='something')


@pytest.fixture
def user_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def user_api_client(user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
    return client


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create(username='admin', password='something', is_staff=True)


@pytest.fixture
def admin_token(admin):
    token, _ = Token.objects.get_or_create(user=admin)
    return token.key


@pytest.fixture
def admin_api_client(admin_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token}')
    return client


@pytest.fixture
def product_factory():
    def factory(min_amount=1, max_amount=20, **kwargs):
        return baker.make('Product', _quantity=randint(min_amount, max_amount), **kwargs)

    return factory


@pytest.fixture
def product_create_payload():
    return {
        'name': 'test',
        'description': 'test',
        'price': 100
    }
