import pytest
from django_webtest import WebTest

from todos_app.models import Todo


@pytest.mark.django_db
def test_todo_detail_something(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    # Todo 1
    resp = django_app.get('/api/todo/{}/'.format(t1.id))

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'

    data = resp.json
    assert data == {
        'id': t1.id,
        'title': 'Test Todo 1',
        'completed': False
    }

    # Todo 2
    resp = django_app.get('/api/todo/{}/'.format(t2.id))

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'

    data = resp.json
    assert data == {
        'id': t2.id,
        'title': 'Test Todo 2',
        'completed': True
    }


@pytest.mark.django_db
def test_todo_detail_not_found(django_app):
    resp = django_app.get('/api/todo/{}/'.format('123456789'), status=404)
    assert resp.status_code == 404
