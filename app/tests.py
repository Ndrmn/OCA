from app import client


def test_test_get():
    res = client.get('/api/test')

    assert res.status_code == 200
    assert len(res.get_json()) > 1


def test_test_post():
    data = {
        'name': 'Unit Tests',
        'description': 'Pytest tutorial'
    }

    res = client.post('/api/test', json=data)

    assert res.status_code == 200
