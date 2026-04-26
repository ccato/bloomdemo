import pytest
from pybloom_live import BloomFilter


def test_bloom_filter_add_and_check():
    """Test basic bloom filter add and check operations."""
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    
    # Add a username
    bf.add('alice')
    
    # Check it exists
    assert 'alice' in bf
    
    # Check non-existent username
    assert 'bob' not in bf


def test_bloom_filter_case_insensitive():
    """Test that bloom filter is case-insensitive."""
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    
    bf.add('Alice')
    
    # Should find lowercase version
    assert 'alice' in bf
    assert 'ALICE' in bf
    assert 'Alice' in bf


def test_bloom_filter_multiple_adds():
    """Test adding multiple usernames."""
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    
    usernames = ['alice', 'bob', 'charlie', 'david', 'eve']
    for username in usernames:
        bf.add(username)
    
    for username in usernames:
        assert username in bf


def test_bloom_filter_false_positive_rate():
    """Test that bloom filter has low false positive rate."""
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    
    # Add 100 usernames
    for i in range(100):
        bf.add(f'user{i}')
    
    # Check 100 non-existent usernames
    false_positives = 0
    for i in range(100, 200):
        if f'user{i}' in bf:
            false_positives += 1
    
    # False positive rate should be very low (< 5% for this test)
    assert false_positives < 5
