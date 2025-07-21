"""Tests for validation utilities."""

import pytest

from flext_target_ldif.validation import (
    ValidationError,
    sanitize_attribute_name,
    validate_attribute_name,
    validate_attribute_value,
    validate_dn_component,
    validate_record,
    validate_schema,
)


class TestValidationError:
    """Test ValidationError exception."""

    def test_validation_error_creation(self) -> None:
        """Test ValidationError can be created and raised."""
        error = ValidationError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

        # Test that it can be raised
        with pytest.raises(ValidationError, match="Test error message"):
            raise ValidationError("Test error message")


class TestValidation:
    """Test cases for validation functions."""

    def test_validate_dn_component(self) -> None:
        """Test DN component validation."""
        # Valid components
        assert validate_dn_component("testuser")
        assert validate_dn_component("user123")
        assert validate_dn_component("test.user")
        assert validate_dn_component("test_user")

        # Invalid components
        assert not validate_dn_component("")
        assert not validate_dn_component("user,name")
        assert not validate_dn_component("user=value")
        assert not validate_dn_component("user+extra")
        assert not validate_dn_component("user<test")
        assert not validate_dn_component("user>test")
        assert not validate_dn_component("user#test")
        assert not validate_dn_component("user;test")
        assert not validate_dn_component('user"test')
        assert not validate_dn_component("user\\test")
        assert not validate_dn_component("user\ntest")

    def test_validate_attribute_name(self) -> None:
        """Test LDAP attribute name validation."""
        # Valid names
        assert validate_attribute_name("uid")
        assert validate_attribute_name("cn")
        assert validate_attribute_name("givenName")
        assert validate_attribute_name("telephoneNumber")
        assert validate_attribute_name("mail")
        assert validate_attribute_name("objectClass")
        assert validate_attribute_name("custom-attribute")

        # Invalid names
        assert not validate_attribute_name("")
        assert not validate_attribute_name("123invalid")  # Starts with number
        assert not validate_attribute_name("invalid_name")  # Contains underscore
        assert not validate_attribute_name("invalid.name")  # Contains dot
        assert not validate_attribute_name("invalid name")  # Contains space
        assert not validate_attribute_name("invalid@name")  # Contains @

    def test_validate_attribute_value(self) -> None:
        """Test attribute value validation."""
        # Valid values
        assert validate_attribute_value("test")
        assert validate_attribute_value(123)
        assert validate_attribute_value(True)
        assert validate_attribute_value(None)
        assert validate_attribute_value("")

        # Test length limit
        long_value = "x" * 1001  # Over the 1000 char limit
        assert not validate_attribute_value(long_value)

        # Reasonable length should be valid
        reasonable_value = "x" * 500
        assert validate_attribute_value(reasonable_value)

    def test_sanitize_attribute_name(self) -> None:
        """Test attribute name sanitization."""
        # Test removing invalid characters
        assert sanitize_attribute_name("user_name") == "username"
        assert sanitize_attribute_name("user.name") == "username"
        assert sanitize_attribute_name("user name") == "username"
        assert sanitize_attribute_name("user@name") == "username"

        # Test fixing names that start with numbers
        assert sanitize_attribute_name("123user") == "attr123user"

        # Test empty name fallback
        assert sanitize_attribute_name("") == "unknownAttr"
        assert sanitize_attribute_name("!!!") == "unknownAttr"

        # Test valid names remain unchanged
        assert sanitize_attribute_name("validName") == "validName"
        assert sanitize_attribute_name("valid-name") == "valid-name"

    def test_validate_record(self) -> None:
        """Test record validation."""
        # Valid record
        valid_record = {
            "uid": "testuser",
            "cn": "Test User",
            "mail": "test@example.com",
        }
        errors = validate_record(valid_record)
        assert len(errors) == 0

        # Empty record
        errors = validate_record({})
        assert "record" in errors

        # Record without ID field
        no_id_record = {
            "name": "Test User",
            "email": "test@example.com",
        }
        errors = validate_record(no_id_record)
        assert "dn" in errors

        # Record with invalid field names
        invalid_record = {
            "123invalid": "value",
            "invalid_field!": "value",
            "uid": "testuser",  # This should be valid
        }
        errors = validate_record(invalid_record)
        assert "123invalid" in errors
        assert "invalid_field!" in errors
        assert "uid" not in errors  # Valid field should not have errors

    def test_validate_schema(self) -> None:
        """Test schema validation."""
        # Valid schema
        valid_schema = {
            "properties": {
                "uid": {"type": "string"},
                "cn": {"type": "string"},
                "mail": {"type": "string"},
            }
        }
        errors = validate_schema(valid_schema)
        assert len(errors) == 0

        # Empty schema
        errors = validate_schema({})
        assert "schema" in errors

        # Schema without properties
        no_props_schema = {"type": "object"}
        errors = validate_schema(no_props_schema)
        assert "properties" in errors

        # Schema without ID fields
        no_id_schema = {
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
            }
        }
        errors = validate_schema(no_id_schema)
        assert "id_fields" in errors

        # Schema with invalid property names
        invalid_schema = {
            "properties": {
                "uid": {"type": "string"},  # Valid
                "123invalid": {"type": "string"},  # Invalid
                "invalid_prop!": {"type": "string"},  # Invalid
            }
        }
        errors = validate_schema(invalid_schema)
        assert "invalid_properties" in errors
        assert len(errors["invalid_properties"]) == 2  # Two invalid properties

    def test_record_with_various_id_fields(self) -> None:
        """Test that various ID field types are recognized."""
        # Test different ID field names
        id_fields = ["id", "uid", "user_id", "username"]

        for id_field in id_fields:
            record = {id_field: "testuser", "name": "Test User"}
            errors = validate_record(record)
            assert "dn" not in errors  # Should not have DN errors

    def test_schema_with_various_id_fields(self) -> None:
        """Test that various ID field types are recognized in schema."""
        id_fields = ["id", "uid", "user_id", "username"]

        for id_field in id_fields:
            schema = {
                "properties": {
                    id_field: {"type": "string"},
                    "name": {"type": "string"},
                }
            }
            errors = validate_schema(schema)
            assert "id_fields" not in errors  # Should not have ID field errors
