import pytest
from app import app


def test_check_username_available(client, empty_bloom, monkeypatch):
    """Test checking a username that is available."""
    # Mock the bloom filter to use our empty one
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', empty_bloom)
    
    response = client.post('/check', json={'username': 'newuser'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['exists'] is False
    assert data['message'] == 'Definitely available'
    assert 'suggestions' not in data


def test_check_username_taken(client, sample_bloom, monkeypatch):
    """Test checking a username that is taken."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', sample_bloom)
    
    response = client.post('/check', json={'username': 'alice'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['exists'] is True
    assert data['message'] == 'Probably taken'
    assert 'suggestions' in data
    assert len(data['suggestions']) > 0


def test_check_username_too_short(client):
    """Test validation for username that is too short."""
    response = client.post('/check', json={'username': 'ab'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Too short'


def test_check_username_case_insensitive(client, sample_bloom, monkeypatch):
    """Test that username check is case-insensitive."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', sample_bloom)
    
    # Add in lowercase
    response1 = client.post('/check', json={'username': 'Alice'})
    assert response1.status_code == 200
    data1 = response1.get_json()
    assert data1['exists'] is True
    
    # Check uppercase version
    response2 = client.post('/check', json={'username': 'ALICE'})
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2['exists'] is True


def test_check_username_whitespace_trimming(client, empty_bloom, monkeypatch):
    """Test that whitespace is trimmed from username."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', empty_bloom)
    
    response = client.post('/check', json={'username': '  newuser  '})
    assert response.status_code == 200
    data = response.get_json()
    assert data['exists'] is False
