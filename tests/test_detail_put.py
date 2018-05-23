import json
import pytest
from django_webtest import WebTest

from todos_app.models import Todo


@pytest.mark.django_db
def test_todo_detail_put_1(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    # Todo 1
    resp = django_app.put('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'title': 'Test Todo 1 - UPDATED',
        'completed': False
    }), content_type='application/json')

    assert resp.status_code == 204

    todo = Todo.objects.get(id=t1.id)
    assert todo.title == 'Test Todo 1 - UPDATED'
    assert todo.completed is False

    # Todo 2
    resp = django_app.put('/api/todo/{}/'.format(t2.id), params=json.dumps({
        'title': 'Test Todo 2 - UPDATED',
        'completed': False
    }), content_type='application/json')

    assert resp.status_code == 204

    todo = Todo.objects.get(id=t2.id)
    assert todo.title == 'Test Todo 2 - UPDATED'
    assert todo.completed is False

    # Todo 3
    resp = django_app.put('/api/todo/{}/'.format(t3.id), params=json.dumps({
        'title': 'Test Todo 3 - UPDATED',
        'completed': True
    }), content_type='application/json')

    assert resp.status_code == 204

    todo = Todo.objects.get(id=t3.id)
    assert todo.title == 'Test Todo 3 - UPDATED'
    assert todo.completed is True



@pytest.mark.django_db
def test_todo_detail_put_incomplete_data_Fails_2(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')

    # Missing the 'completed' argument makes the request fail
    resp = django_app.put('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'title': 'Test Todo 1 - UPDATED'
    }), content_type='application/json', status=400)
    assert resp.status_code == 400
    assert resp.json == {
        'error': 'Missing argument: completed'
    }

    # Missing the 'title' argument makes the request fail
    resp = django_app.put('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'completed': True
    }), content_type='application/json', status=400)
    assert resp.status_code == 400
    assert resp.json == {
        'error': 'Missing argument: title'
    }


@pytest.mark.django_db
def test_todo_detail_put_not_found_3(django_app):
    resp = django_app.put('/api/todo/{}/'.format('1234567894564654'), params=json.dumps({
        'title': 'NO TODO :()'
    }), content_type='application/json', status=404)

    assert resp.status_code == 404
