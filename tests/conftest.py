import os
import django
import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_testing.settings')
django.setup()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory