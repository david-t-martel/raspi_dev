import pytest
from dashboard.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b'Login' in rv.data

def test_invalid_login(client):
    rv = client.post('/login', data={
        'username': 'wrong',
        'password': 'wrong'
    })
    assert b'Login' in rv.data