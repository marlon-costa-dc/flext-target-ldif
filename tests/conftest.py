"""Pytest configuration and fixtures for FLEXT Target LDIF tests."""

import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def temp_dir() -> Generator[Path]:
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def temp_file() -> Generator[Path]:
    """Provide a temporary file for tests."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        yield temp_path
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()


@pytest.fixture
def sample_config(temp_dir: Path) -> dict[str, Any]:
    """Provide a sample configuration for testing."""
    return {
        "output_path": str(temp_dir),
        "file_naming_pattern": "{stream_name}_{timestamp}.ldif",
        "dn_template": "uid={uid},ou=users,dc=example,dc=com",
        "ldif_options": {
            "line_length": 78,
            "base64_encode": False,
            "include_timestamps": True,
        },
        "attribute_mapping": {
            "user_id": "uid",
            "full_name": "cn",
            "email": "mail",
        },
    }


@pytest.fixture
def sample_record() -> dict[str, str]:
    """Provide a sample record for testing."""
    return {
        "uid": "testuser",
        "cn": "Test User",
        "givenName": "Test",
        "sn": "User",
        "mail": "test@example.com",
        "telephoneNumber": "+1-555-123-4567",
        "title": "Software Engineer",
        "departmentNumber": "Engineering",
    }


@pytest.fixture
def sample_schema() -> dict[str, Any]:
    """Provide a sample Singer schema for testing."""
    return {
        "type": "object",
        "properties": {
            "uid": {"type": "string"},
            "cn": {"type": "string"},
            "givenName": {"type": "string"},
            "sn": {"type": "string"},
            "mail": {"type": "string"},
            "telephoneNumber": {"type": "string"},
            "title": {"type": "string"},
            "departmentNumber": {"type": "string"},
        },
        "required": ["uid", "cn", "sn"],
    }


@pytest.fixture
def multiple_records() -> list[dict[str, str]]:
    """Provide multiple sample records for testing."""
    return [
        {
            "uid": "user1",
            "cn": "User One",
            "givenName": "User",
            "sn": "One",
            "mail": "user1@example.com",
        },
        {
            "uid": "user2",
            "cn": "User Two",
            "givenName": "User",
            "sn": "Two",
            "mail": "user2@example.com",
        },
        {
            "uid": "user3",
            "cn": "User Three",
            "givenName": "User",
            "sn": "Three",
            "mail": "user3@example.com",
        },
    ]


@pytest.fixture
def ldif_options() -> dict[str, Any]:
    """Provide sample LDIF options for testing."""
    return {
        "line_length": 78,
        "base64_encode": False,
        "include_timestamps": True,
    }


@pytest.fixture
def attribute_mapping() -> dict[str, str]:
    """Provide sample attribute mapping for testing."""
    return {
        "user_id": "uid",
        "username": "uid",
        "full_name": "cn",
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
        "phone": "telephoneNumber",
        "job_title": "title",
        "department": "departmentNumber",
    }


# Pytest markers for test categorization
def pytest_configure(config: Any) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "ldif: mark test as LDIF-specific")
    config.addinivalue_line("markers", "singer: mark test as Singer-specific")
    config.addinivalue_line("markers", "target: mark test as target-specific")
    config.addinivalue_line("markers", "sink: mark test as sink-specific")
    config.addinivalue_line(
        "markers",
        "requires_filesystem: mark test as requiring file system access",
    )
