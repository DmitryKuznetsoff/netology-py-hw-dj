from random import randint

import pytest
from model_bakery import baker


@pytest.fixture
def student_factory():
    def factory(min_amount=1, max_amount=20, **kwargs):
        return baker.make('Student', _quantity=randint(min_amount, max_amount), **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(min_amount=1, max_amount=20, **kwargs):
        return baker.make('Course', _quantity=randint(min_amount, max_amount), **kwargs)

    return factory
