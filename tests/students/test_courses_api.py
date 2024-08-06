import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from model_bakery import baker

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('students.Course', **kwargs)
    return factory

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-list')
    response = api_client.get(url, {'id': course.id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course = course_factory(name='Unique Course Name')
    url = reverse('courses-list')
    response = api_client.get(url, {'name': 'Unique Course Name'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == course.name

@pytest.mark.django_db
def test_create_course(api_client):
    url = reverse('courses-list')
    data = {'name': 'New Course'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    data = {'name': 'Updated Course'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == 204