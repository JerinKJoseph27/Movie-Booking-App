import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import validate_name, validate_phone

# Test name validation
print("=== Name Validation Tests ===")
test_names = [
    "John Doe",           # Valid
    "Mary Jane",          # Valid
    "A",                  # Too short
    "John123",            # Contains numbers
    "John O'Connor",      # Valid with apostrophe
    "Dr. Smith",          # Valid with dot
    "Jean-Pierre",        # Valid with hyphen
    "",                   # Empty
    "A" * 51,            # Too long
]

for name in test_names:
    valid, message = validate_name(name)
    print(f"'{name}': {'✓' if valid else '✗'} {message}")

print("\n=== Phone Validation Tests ===")
test_phones = [
    "9876543210",         # Valid 10-digit
    "8123456789",         # Valid 10-digit starting with 8
    "5123456789",         # Invalid - doesn't start with 6,7,8,9
    "919876543210",       # Valid with country code
    "02212345678",        # Valid with STD code
    "123",                # Too short
    "+91 98765 43210",    # Valid with formatting
    "98-7654-3210",       # Valid with dashes
    "",                   # Empty
    "abcd123456",         # Contains letters
]

for phone in test_phones:
    valid, message = validate_phone(phone)
    print(f"'{phone}': {'✓' if valid else '✗'} {message}")
