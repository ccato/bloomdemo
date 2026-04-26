import pytest
from app import generate_suggestions
from pybloom_live import BloomFilter


def test_generate_suggestions_basic(empty_bloom, monkeypatch):
    """Test basic suggestion generation."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', empty_bloom)
    
    suggestions = generate_suggestions('test', count=3)
    
    assert len(suggestions) == 3
    assert all(s.startswith('test') for s in suggestions)
    # All suggestions should be unique
    assert len(set(suggestions)) == 3


def test_generate_suggestions_avoids_taken(monkeypatch):
    """Test that suggestions avoid usernames already in bloom filter."""
    bf = BloomFilter(capacity=1000, error_rate=0.001)
    bf.add('alice_dev10')
    bf.add('alice_x20')
    
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', bf)
    
    suggestions = generate_suggestions('alice', count=3)
    
    # Suggestions should not be in the bloom filter
    for suggestion in suggestions:
        assert suggestion not in bf


def test_generate_suggestions_count(empty_bloom, monkeypatch):
    """Test that requested count is respected."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', empty_bloom)
    
    for count in [1, 3, 5]:
        suggestions = generate_suggestions('test', count=count)
        assert len(suggestions) == count


def test_generate_suggestions_suffixes(empty_bloom, monkeypatch):
    """Test that suggestions use expected suffixes."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', empty_bloom)
    
    suggestions = generate_suggestions('test', count=10)
    
    # Check that suggestions have expected patterns
    suffixes = ["_dev", "x", "_pro", "2026", "real"]
    for suggestion in suggestions:
        has_suffix = any(suffix in suggestion for suffix in suffixes)
        assert has_suffix, f"Suggestion {suggestion} doesn't have expected suffix"


def test_generate_suggestions_with_numbers(empty_bloom, monkeypatch):
    """Test that suggestions include random numbers."""
    import app as app_module
    monkeypatch.setattr(app_module, 'bloom', empty_bloom)
    
    suggestions = generate_suggestions('test', count=10)
    
    # All suggestions should end with numbers
    for suggestion in suggestions:
        assert suggestion[-2:].isdigit(), f"Suggestion {suggestion} doesn't end with numbers"
