import json
import pytest
from django_webtest import WebTest

from todos_app.models import Todo


@pytest.mark.django_db
def test_todo_detail_patch_values_1(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    # Todo 1: title
    resp = django_app.patch('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'title': 'Test Todo 1 - UPDATED'
    }), content_type='application/json')

    todo = Todo.objects.get(id=t1.id)
    assert todo.title == 'Test Todo 1 - UPDATED'
    assert todo.completed is False  # Hasn't changed

    # Todo 1: completed
    resp = django_app.patch('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'completed': True
    }), content_type='application/json')

    todo = Todo.objects.get(id=t1.id)
    assert todo.title == 'Test Todo 1 - UPDATED'  # Hasn't changed
    assert todo.completed is True

    # Todo 2: title
    resp = django_app.patch('/api/todo/{}/'.format(t2.id), params=json.dumps({
        'title': 'Test Todo 2 - UPDATED'
    }), content_type='application/json')

    todo = Todo.objects.get(id=t2.id)
    assert todo.title == 'Test Todo 2 - UPDATED'
    assert todo.completed is True  # Hasn't changed

    # Todo 2: completed
    resp = django_app.patch('/api/todo/{}/'.format(t2.id), params=json.dumps({
        'completed': False
    }), content_type='application/json')

    todo = Todo.objects.get(id=t2.id)
    assert todo.title == 'Test Todo 2 - UPDATED'
    assert todo.completed is False  # Hasn't changed


@pytest.mark.django_db
def test_todo_detail_patch_action_2(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    # Todo 1: First toggle
    resp = django_app.patch('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'action': 'toggle'
    }), content_type='application/json')

    assert Todo.objects.get(id=t1.id).completed is True

    # Todo 1: Second toggle
    resp = django_app.patch('/api/todo/{}/'.format(t1.id), params=json.dumps({
        'action': 'toggle'
    }), content_type='application/json')

    assert Todo.objects.get(id=t1.id).completed is False


    # Todo 2: First toggle
    resp = django_app.patch('/api/todo/{}/'.format(t2.id), params=json.dumps({
        'action': 'toggle'
    }), content_type='application/json')

    assert Todo.objects.get(id=t2.id).completed is False

    # Todo 2: Second toggle
    resp = django_app.patch('/api/todo/{}/'.format(t2.id), params=json.dumps({
        'action': 'toggle'
    }), content_type='application/json')

    assert Todo.objects.get(id=t2.id).completed is True


@pytest.mark.django_db
def test_todo_detail_patch_not_found_3(django_app):
    resp = django_app.patch('/api/todo/{}/'.format('1236549879821'), params=json.dumps({
        'title': 'NO TODO :()'
    }), content_type='application/json', status=404)

    assert resp.status_code == 404
