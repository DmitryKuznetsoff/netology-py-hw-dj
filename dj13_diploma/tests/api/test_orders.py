import random

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from api.models import OrderStatusChoices


@pytest.mark.django_db
def test_order_retrieve(order_factory, user_api_client):
    order = order_factory()[0]
    url = reverse('orders-detail', args=[order.id])

    resp = user_api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    assert order.id == resp_json['id']


@pytest.mark.django_db
def test_order_list(order_factory, user_api_client):
    orders_list = order_factory()
    url = reverse('orders-list')

    resp = user_api_client.get(url)
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    expected_ids = {order.id for order in orders_list}
    response_ids = {order['id'] for order in resp_json}
    assert expected_ids == response_ids


@pytest.mark.django_db
def test_order_filter_by_status(order_factory, admin_api_client):
    orders_list = order_factory()
    random_status = random.choices(OrderStatusChoices.names)
    url = reverse('orders-list')

    resp = admin_api_client.get(url, {'status': random_status})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    expected_ids = {order.id for order in orders_list if order.status == random_status}
    resp_ids = {order.get('id') for order in resp_json}
    assert expected_ids == resp_ids


@pytest.mark.django_db
def test_order_filter_by_order_sum(order_factory, admin_api_client):
    random_order_sum = random.choices(order_factory())[0].order_sum
    url = reverse('orders-list')

    resp = admin_api_client.get(url, {'order_sum_min': random_order_sum, 'order_sum_max': random_order_sum})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    order_sum = {order['order_sum'] for order in resp_json}
    check_order_sum = set(filter(lambda x: x == random_order_sum, order_sum))
    assert order_sum == check_order_sum


@pytest.mark.django_db
def test_order_filter_by_creation_date(order_factory, admin_api_client):
    random_order_creation_date = random.choice(order_factory()).created_at
    url = reverse('orders-list')

    resp = admin_api_client.get(url, {'created_at': random_order_creation_date})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    creation_dates = {order['created_at'] for order in resp_json}
    check_order_creation_date = set(filter(lambda x: x == random_order_creation_date.isoformat(), creation_dates))
    assert creation_dates == check_order_creation_date


@pytest.mark.django_db
def test_order_filter_by_update_date(order_factory, admin_api_client):
    random_order_update_date = random.choice(order_factory()).created_at
    url = reverse('orders-list')

    resp = admin_api_client.get(url, {'created_at': random_order_update_date})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    update_dates = {order['created_at'] for order in resp_json}
    check_order_update_date = set(filter(lambda x: x == random_order_update_date.isoformat(), update_dates))
    assert update_dates == check_order_update_date


@pytest.mark.django_db
def test_order_filter_by_product(order_factory, admin_api_client):
    random_order = random.choice(order_factory())
    random_product = random.choice(random_order.products.all())
    url = reverse('orders-list')

    resp = admin_api_client.get(url, {'product_id': random_product.id})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    resp_orders = {order['id'] for order in resp_json}
    check_resp_orders = set()
    for order in resp_json:
        if [position for position in order['positions'] if position['product_id'] == random_product.id]:
            check_resp_orders.add(order['id'])
    assert resp_orders == check_resp_orders


@pytest.mark.django_db
def test_order_create(user_api_client, order_create_payload):
    url = reverse('orders-list')

    resp = user_api_client.post(url, data=order_create_payload, format='json')
    assert resp.status_code == HTTP_201_CREATED

    resp_json = resp.json()
    assert resp_json['positions'][0]['product_id'] == order_create_payload['positions'][0]['product_id'] and \
           resp_json['positions'][0]['amount'] == order_create_payload['positions'][0]['amount']


@pytest.mark.django_db
def test_order_update_by_owner(user_api_client, order_factory, user):
    order = order_factory()[0]
    order.user = user
    url = reverse('orders-detail', args=[order.id])
    product_id = order.positions.first().product_id
    amount = order.positions.first().amount + 1

    resp = user_api_client.patch(url, data={'positions': [{'product_id': product_id, 'amount': amount}]})
    assert resp.status_code == HTTP_200_OK

    resp_json = resp.json()
    check_positions = [position['product_id'] for position in resp_json['positions'] if
                       position['product_id'] == product_id and position['amount'] == amount
                       ]
    assert check_positions


@pytest.mark.django_db
def test_order_update_by_another_user(user, another_user_api_client, order_factory):
    order = order_factory()[0]
    url = reverse('orders-detail', args=[order.id])
    product_id = order.positions.first().product_id
    amount = order.positions.first().amount + 1

    resp = another_user_api_client.patch(url, data={'positions': [{'product_id': product_id, 'amount': amount}]})
    assert resp.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_order_delete_by_owner(user_api_client, order_factory):
    random_order = random.choices(order_factory())[0]
    url = reverse('orders-detail', args=[random_order.id])

    resp = user_api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT

    existing_ids = [order['id'] for order in user_api_client.get(reverse('orders-list')).json()]
    assert random_order.id not in existing_ids


@pytest.mark.django_db
def test_order_delete_by_another_user(another_user_api_client, order_factory):
    random_order = random.choices(order_factory())[0]
    url = reverse('orders-detail', args=[random_order.id])

    resp = another_user_api_client.delete(url)
    assert resp.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_order_delete_by_admin(order_factory, admin_api_client):
    random_order = random.choices(order_factory())[0]
    url = reverse('orders-detail', args=[random_order.id])

    resp = admin_api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT

    existing_ids = [order['id'] for order in admin_api_client.get(reverse('orders-list')).json()]
    assert random_order.id not in existing_ids
