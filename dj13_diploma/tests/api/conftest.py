from random import randint

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product_factory():
    def factory(min_amount=1, max_amount=20, **kwargs):
        return baker.make('Product', _quantity=randint(min_amount, max_amount), **kwargs)

    return factory
