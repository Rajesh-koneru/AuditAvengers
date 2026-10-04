import pytest
from unittest.mock import patch, MagicMock
from audit_tracker import create_App

flask_app = create_App()

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.secret_key = 'test_secret'
    with flask_app.test_client() as client:
        yield client

@patch('audit_tracker.auth.get_connection')
def test_signup_validation_mismatch_passwords(mock_get_conn, client):
    response = client.post('/signup', json={
        'auditor_name': 'New Auditor',
        'email': 'auditor@example.com',
        'phone': '9876543210',
        'password': 'password123',
        'confirm_password': 'password456'
    })
    assert response.status_code == 400
    assert 'Passwords do not match' in response.get_json()['error']

@patch('audit_tracker.auth.get_connection')
def test_signup_success(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    with patch('audit_tracker.apply.generate_auditor_id', return_value='AUD100'):
        response = client.post('/signup', json={
            'auditor_name': 'New Auditor',
            'email': 'auditor@example.com',
            'phone': '9876543210',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        assert response.status_code == 200
        assert 'Registration successful' in response.get_json()['message']
