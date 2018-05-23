import pytest
from django_webtest import WebTest

from todos_app.models import Todo


@pytest.mark.django_db
def test_todo_list_1(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    resp = django_app.get('/api/todo/')

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'

    data = resp.json
    assert data == {
        'filter': 'all',
        'count': 3,
        'results': [{
            'id': t3.id,
            'title': 'Test Todo 3',
            'completed': False
        }, {
            'id': t2.id,
            'title': 'Test Todo 2',
            'completed': True
        }, {
            'id': t1.id,
            'title': 'Test Todo 1',
            'completed': False
        }]
    }


@pytest.mark.django_db
def test_todo_list_filter_active_2(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    resp = django_app.get('/api/todo/?status=active')

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'

    data = resp.json
    assert data == {
        'filter': 'active',
        'count': 2,
        'results': [{
            'id': t3.id,
            'title': 'Test Todo 3',
            'completed': False
        }, {
            'id': t1.id,
            'title': 'Test Todo 1',
            'completed': False
        }]
    }


@pytest.mark.django_db
def test_todo_list_filter_completed_3(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    resp = django_app.get('/api/todo/?status=completed')

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'

    data = resp.json
    assert data == {
        'filter': 'completed',
        'count': 1,
        'results': [{
            'id': t2.id,
            'title': 'Test Todo 2',
            'completed': True
        }]
    }
