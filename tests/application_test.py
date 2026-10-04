import pytest
from unittest.mock import patch, MagicMock
from audit_tracker import create_App

flask_app = create_App()

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.secret_key = 'test_secret'
    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
            sess['Audit_id'] = 'AUD123'
            sess['whatsappLink'] = 'https://wa.me/1234567890'
        yield client

@patch('audit_tracker.apply.get_connection')
def test_application_submission(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        'Audit_id': 'AUD123',
        'Audit_type': 'Financial',
        'Date': '2025-04-16',
        'Client_id': 'CL001',
        'state': 'Telangana'
    }

    response = client.post(
        '/apply/audit_application',
        json={
            'name': 'John Doe',
            'phone': '9876543210',
            'email': 'john@example.com'
        }
    )

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Your application has been submitted successfully!'

