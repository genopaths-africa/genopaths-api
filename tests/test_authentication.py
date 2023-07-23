def test_login(client):
    response = client.post('/api/auth/login', json={'username': 'admin@genopaths.africa', 'password': 'Password@9'})
    assert response.status_code == 200
    assert response.json['data']['first_name'] == 'admin'
    assert response.json['status'] == 'success'

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'user@genopaths.africa',
        'first_name': 'Firstname',
        'role': 'admin',
        'last_name': 'Lastname',
        'other_names': 'Othernames',
        'password': 'Password@9',
        'confirm_password': 'Password@9',
        'phone_number': '00000000',
        'job_title': 'Researcher'
    })

    assert response.status_code == 200