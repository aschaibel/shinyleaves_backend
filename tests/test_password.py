import pytest
from app.utils.password import password_hash, verify_password

def test_password_hash():
    """Test that password_hash returns a string."""
    password = "test_password"
    hashed = password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password  # Ensure the hash is different from the original password

def test_verify_password():
    """Test that verify_password correctly verifies passwords."""
    password = "test_password"
    hashed = password_hash(password)
    
    # Test correct password
    assert verify_password(password, hashed) is True
    
    # Test incorrect password
    assert verify_password("wrong_password", hashed) is False

def test_different_passwords_different_hashes():
    """Test that different passwords produce different hashes."""
    password1 = "test_password1"
    password2 = "test_password2"
    
    hash1 = password_hash(password1)
    hash2 = password_hash(password2)
    
    assert hash1 != hash2

def test_same_password_different_hashes():
    """Test that the same password produces different hashes due to salt."""
    password = "test_password"
    
    hash1 = password_hash(password)
    hash2 = password_hash(password)
    
    assert hash1 != hash2  # Bcrypt uses random salt, so hashes should be different