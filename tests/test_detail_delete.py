import pytest
from django_webtest import WebTest

from todos_app.models import Todo


@pytest.mark.django_db
def test_delete_todo_1(django_app):
    t1 = Todo.objects.create(title='Test Todo 1')
    t2 = Todo.objects.create(title='Test Todo 2', completed=True)
    t3 = Todo.objects.create(title='Test Todo 3')

    # Todo 1
    resp = django_app.delete('/api/todo/{}/'.format(t1.id))
    assert resp.status_code == 204

    # Todo should be deleted
    assert Todo.objects.count() == 2

    # Todo 1
    resp = django_app.delete('/api/todo/{}/'.format(t2.id))
    assert resp.status_code == 204

    # Todo should be deleted
    assert Todo.objects.count() == 1


@pytest.mark.django_db
def test_delete_todo_not_found_2(django_app):
    # Todo 1
    resp = django_app.delete('/api/todo/{}/'.format('12365478963258741'), status=404)
    assert resp.status_code == 404
