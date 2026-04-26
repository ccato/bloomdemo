import pytest
from app import app, bloom, generate_suggestions
from pybloom_live import BloomFilter


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def empty_bloom():
    """Create a fresh empty bloom filter for testing."""
    return BloomFilter(capacity=1000, error_rate=0.001)


@pytest.fixture
def sample_bloom():
    """Create a bloom filter with sample usernames."""
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    sample_usernames = ["alice", "bob", "charlie", "david", "eve"]
    for username in sample_usernames:
        bf.add(username.lower())
    return bf
