from app import client


def test_login_and_auth():

    res = client.post('/register', json={"name": "test_from_testing",
                                         "email": "test@ukr.net", "password": "testpass"})
    assert res.status_code == 200

    log = client.post(
        '/register', json={"name": "test_from_testing", "password": "testpass"})
    assert res.status_code == 200
    test_auth = client.post('/test_auth_api', headers={
                           'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MTM1MTI1NCwianRpIjoiZGM5Njk2ZDItZTc2Ny00NmViLWI0MzItNDk3MzRlMGIzYzZkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNjcxMzUxMjU0LCJleHAiOjE2NzM0MjQ4NTR9.wJYReeuxV5pRZwSIlFw5cBKnCJ4lX6_OS3DiOdIq6lE'})
    assert test_auth.status_code == 200


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
