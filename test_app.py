from app import app

import pytest

@pytest.fixture


def client():
    ''' create a test client that can send requests to the API without running the actual server '''
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response  = client.get('/')
    assert response.status_code == 200
    assert response.json == {'Message': 'Hello TextToAudio API'}


