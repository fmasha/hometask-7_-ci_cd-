from app import app

def test_index():
    resp1 = app.test_client().get('/')
    assert resp1.status_code == 200

def test_add():
    resp2 = app.test_client().post('/add', data={'todo_item': 1234})
    assert resp2.status_code == 302
