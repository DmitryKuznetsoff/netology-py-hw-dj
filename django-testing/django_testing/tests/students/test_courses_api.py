import random

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_course_retrieve(api_client, course_factory, student_factory):
    course = course_factory(min_amount=1, max_amount=1, students=student_factory())[0]
    url = reverse('courses-detail', args=[course.id])

    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == course.id


@pytest.mark.django_db
def test_course_list(api_client, course_factory, student_factory):
    courses_list = course_factory(students=student_factory())
    url = reverse('courses-list')

    resp = api_client.get(url)
    resp_json = resp.json()

    expected_ids = {course.id for course in courses_list}
    response_ids = {course['id'] for course in resp_json}

    assert resp.status_code == HTTP_200_OK
    assert response_ids == expected_ids


@pytest.mark.django_db
def test_course_filter_by_id(api_client, course_factory, student_factory):
    courses_list = course_factory(students=student_factory())
    random_course_id = random.choice(courses_list).id
    url = reverse('courses-list')

    resp = api_client.get(url, {'id': random_course_id})
    resp_json = resp.json()[0]

    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == random_course_id


@pytest.mark.django_db
def test_course_filter_by_name(api_client, course_factory, student_factory):
    courses_list = course_factory(students=student_factory())
    random_course_name = random.choice(courses_list).name
    url = reverse('courses-list')

    resp = api_client.get(url, {'name': random_course_name})
    resp_json = resp.json()[0]

    assert resp.status_code == HTTP_200_OK
    assert resp_json['name'] == random_course_name


@pytest.mark.django_db
def test_course_create(api_client, student_factory):
    url = reverse('courses-list')
    students = student_factory()
    student_ids = [student.id for student in students]
    payload = {
        'name': 'test',
        'students': student_ids
    }

    resp = api_client.post(url, payload, format="json")
    resp_json = resp.json()

    assert resp.status_code == HTTP_201_CREATED
    assert resp_json['name'] == payload['name'] and resp_json['students'] == student_ids


@pytest.mark.django_db
def test_course_update(api_client, course_factory, student_factory):
    courses_list = course_factory(students=student_factory())
    random_curse = random.choice(courses_list)
    url = reverse('courses-detail', args=[random_curse.id])
    payload = {
        'name': f'{random_curse.name}_test'
    }

    resp = api_client.patch(url, payload, format='json')
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == random_curse.id and resp_json['name'] == payload['name']


@pytest.mark.django_db
def test_course_delete(api_client, course_factory, student_factory):
    courses_list = course_factory(students=student_factory())
    random_curse_id = random.choice(courses_list).id
    url = reverse('courses-detail', args=[random_curse_id])

    resp = api_client.delete(url)
    existing_ids = [course['id'] for course in api_client.get(reverse('courses-list')).json()]

    assert resp.status_code == HTTP_204_NO_CONTENT
    assert random_curse_id not in existing_ids


@pytest.mark.parametrize(
    ['students_per_course', 'expected_value'],
    (
            (20, True),
            (21, False),
            (-4, False)
    )
)
def test_with_specific_settings(settings, students_per_course, expected_value):
    value_to_compare = settings.MAX_STUDENTS_PER_COURSE
    settings.MAX_STUDENTS_PER_COURSE = students_per_course

    result = 0 <= students_per_course <= value_to_compare

    assert result == expected_value
