import pytest

def test_empty_response(client):
    response = client.get('/api/users')
    print(response.json)
    assert response.json == []
    assert response.status_code == 200
