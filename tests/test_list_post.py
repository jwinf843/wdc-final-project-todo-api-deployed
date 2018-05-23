import json
import pytest
from django_webtest import WebTest

from todos_app.models import Todo


@pytest.mark.django_db
def test_todo_post_only_title_1(django_app):
    # Preconditions: No TODOs created
    assert Todo.objects.count() == 0

    resp = django_app.post('/api/todo/', params=json.dumps({
        'title': 'Testing Todo 1'
    }), content_type='application/json')

    assert resp.status_code == 201
    assert resp.content_type == 'application/json'

    # Postconditions: Todo exists
    assert Todo.objects.count() == 1

    todo = Todo.objects.last()
    assert todo.title == 'Testing Todo 1'
    assert todo.completed == False


@pytest.mark.django_db
def test_todo_post_title_completed_2(django_app):
    # Preconditions: No TODOs created
    assert Todo.objects.count() == 0

    resp = django_app.post('/api/todo/', params=json.dumps({
        'title': 'Testing Todo 1',
        'completed': True
    }), content_type='application/json')

    assert resp.status_code == 201
    assert resp.content_type == 'application/json'

    # Postconditions: Todo exists
    assert Todo.objects.count() == 1

    todo = Todo.objects.last()
    assert todo.title == 'Testing Todo 1'
    assert todo.completed == True


@pytest.mark.django_db
def test_todo_post_missing_required_params_3(django_app):
    # Preconditions: No TODOs created
    assert Todo.objects.count() == 0

    resp = django_app.post(
        '/api/todo/', params=json.dumps({}),
        content_type='application/json', status=400)
    assert resp.status_code == 400

    # Postconditions: No TODOs created
    assert Todo.objects.count() == 0
