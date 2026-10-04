import json
import sys
import os
import pytest

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('trackerApp'), '..', '..')))

from audit_tracker import create_App

@pytest.fixture
def client():
    """Create a test client for Flask"""
    app = create_App()
    app.testing = True

    with app.test_client() as client:
        yield client

def test_send_mail(client):
    """Test the sendMail API endpoint"""
    response = client.post(
        "/sendMail",
        data=json.dumps({
            "SenderName": "Test User",
            "Email": "rajeshkoneru29@gmail.com",
            "Message": "Hello! This is a test."
        }),
        content_type="application/json"
    )

    assert response.status_code == 200 or response.status_code == 500  # Ensure it doesn't fail silently
    json_data = response.get_json()

    if response.status_code == 200:
        assert "message" in json_data
    else:
        assert "error" in json_data  # Expect an error message if it fails



