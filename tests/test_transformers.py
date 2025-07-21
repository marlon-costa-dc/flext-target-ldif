"""Tests for data transformation utilities."""

from datetime import datetime
from typing import Any

import pytest

from flext_target_ldif.transformers import (
    RecordTransformer,
    normalize_attribute_value,
    transform_boolean,
    transform_email,
    transform_name,
    transform_phone,
    transform_timestamp,
)


class TestTransformTimestamp:
    """Test timestamp transformation functions."""

    def test_none_value(self) -> None:
        assert transform_timestamp(None) == ""

    def test_datetime_object(self) -> None:
        dt = datetime(2023, 12, 25, 14, 30, 45)
        result = transform_timestamp(dt)
        assert result == "20231225143045Z"

    def test_iso_string(self) -> None:
        result = transform_timestamp("2023-12-25T14:30:45Z")
        assert result == "20231225143045Z"

    def test_iso_string_without_z(self) -> None:
        result = transform_timestamp("2023-12-25T14:30:45")
        assert result == "20231225143045Z"

    def test_invalid_string(self) -> None:
        result = transform_timestamp("invalid-date")
        assert result == "invalid-date"

    def test_other_type(self) -> None:
        result = transform_timestamp(12345)
        assert result == "12345"


class TestTransformBoolean:
    """Test boolean transformation functions."""

    def test_none_value(self) -> None:
        assert transform_boolean(None) == ""

    def test_true_boolean(self) -> None:
        assert transform_boolean(True) == "TRUE"

    def test_false_boolean(self) -> None:
        assert transform_boolean(False) == "FALSE"

    @pytest.mark.parametrize("value", ["true", "yes", "1", "on", "TRUE", "YES"])
    def test_true_strings(self, value: str) -> None:
        assert transform_boolean(value) == "TRUE"

    @pytest.mark.parametrize("value", ["false", "no", "0", "off", "FALSE", "NO"])
    def test_false_strings(self, value: str) -> None:
        assert transform_boolean(value) == "FALSE"

    def test_other_string(self) -> None:
        result = transform_boolean("maybe")
        assert result == "maybe"

    def test_other_type(self) -> None:
        result = transform_boolean(42)
        assert result == "42"


class TestTransformEmail:
    """Test email transformation functions."""

    def test_none_value(self) -> None:
        assert transform_email(None) == ""

    def test_valid_email(self) -> None:
        result = transform_email("user@example.com")
        assert result == "user@example.com"

    def test_email_with_whitespace(self) -> None:
        result = transform_email("  USER@EXAMPLE.COM  ")
        assert result == "user@example.com"

    def test_invalid_email_no_at(self) -> None:
        assert transform_email("userexample.com") == ""

    def test_invalid_email_no_dot(self) -> None:
        assert transform_email("user@example") == ""

    def test_empty_string(self) -> None:
        assert transform_email("") == ""


class TestTransformPhone:
    """Test phone transformation functions."""

    def test_none_value(self) -> None:
        assert transform_phone(None) == ""

    def test_formatted_phone(self) -> None:
        result = transform_phone("+1 (555) 123-4567")
        assert result == "+1 (555) 123-4567"

    def test_digits_only(self) -> None:
        result = transform_phone("15551234567")
        assert result == "15551234567"

    def test_mixed_format(self) -> None:
        result = transform_phone("555.123.4567 ext 123")
        assert result == "5551234567  123"

    def test_empty_string(self) -> None:
        assert transform_phone("") == ""


class TestTransformName:
    """Test name transformation functions."""

    def test_none_value(self) -> None:
        assert transform_name(None) == ""

    def test_single_name(self) -> None:
        assert transform_name("john") == "John"

    def test_multiple_names(self) -> None:
        assert transform_name("john doe smith") == "John Doe Smith"

    def test_mixed_case(self) -> None:
        assert transform_name("jOHN dOE") == "John Doe"

    def test_whitespace(self) -> None:
        assert transform_name("  john   doe  ") == "John Doe"

    def test_empty_string(self) -> None:
        assert transform_name("") == ""


class TestNormalizeAttributeValue:
    """Test attribute value normalization."""

    def test_none_value(self) -> None:
        assert normalize_attribute_value("any", None) == ""

    def test_email_attribute(self) -> None:
        result = normalize_attribute_value("mail", "USER@EXAMPLE.COM")
        assert result == "user@example.com"

    def test_phone_attribute(self) -> None:
        result = normalize_attribute_value("telephoneNumber", "+1-555-123-4567")
        assert result == "+1-555-123-4567"

    def test_name_attribute(self) -> None:
        result = normalize_attribute_value("givenName", "john")
        assert result == "John"

    def test_timestamp_attribute(self) -> None:
        dt = datetime(2023, 12, 25, 14, 30, 45)
        result = normalize_attribute_value("createTimestamp", dt)
        assert result == "20231225143045Z"

    def test_boolean_attribute(self) -> None:
        result = normalize_attribute_value("isActive", True)
        assert result == "TRUE"

    def test_custom_transformer(self) -> None:
        transformers = {"custom": lambda x: f"custom_{x}"}
        result = normalize_attribute_value("custom", "value", transformers)
        assert result == "custom_value"

    def test_default_transformation(self) -> None:
        result = normalize_attribute_value("unknown", "  value  ")
        assert result == "value"


class TestRecordTransformer:
    """Test record transformer class."""

    def test_init_default(self) -> None:
        transformer = RecordTransformer()
        assert transformer.attribute_mapping == {}
        assert transformer.custom_transformers == {}

    def test_init_with_params(self) -> None:
        mapping = {"field1": "attr1"}
        transformers = {"attr1": lambda x: f"custom_{x}"}
        transformer = RecordTransformer(mapping, transformers)
        assert transformer.attribute_mapping == mapping
        assert transformer.custom_transformers == transformers

    def test_transform_record_basic(self) -> None:
        transformer = RecordTransformer()
        record = {"user_name": "John Doe", "email_address": "john@example.com"}
        result = transformer.transform_record(record)

        assert "username" in result
        assert "emailaddress" in result
        assert result["emailaddress"] == "john@example.com"

    def test_transform_record_with_mapping(self) -> None:
        mapping = {"user_name": "cn", "email_address": "mail"}
        transformer = RecordTransformer(attribute_mapping=mapping)
        record = {"user_name": "John Doe", "email_address": "JOHN@EXAMPLE.COM"}
        result = transformer.transform_record(record)

        assert "cn" in result
        assert "mail" in result
        assert result["mail"] == "john@example.com"

    def test_transform_record_skip_none(self) -> None:
        transformer = RecordTransformer()
        record = {"name": "John", "email": None, "phone": ""}
        result = transformer.transform_record(record)

        assert "name" in result
        assert "email" not in result
        assert "phone" not in result  # Empty string after transformation

    def test_transform_record_with_custom_transformers(self) -> None:
        transformers = {"name": lambda x: x.upper()}
        transformer = RecordTransformer(custom_transformers=transformers)
        record = {"name": "john"}
        result = transformer.transform_record(record)

        assert result["name"] == "JOHN"

    def test_add_required_attributes_default(self) -> None:
        transformer = RecordTransformer()
        record = {"uid": "jdoe"}
        result = transformer.add_required_attributes(record)

        assert "objectclass" in result
        assert result["objectclass"] == ["inetOrgPerson", "person"]
        assert "cn" in result
        assert result["cn"] == "jdoe"
        assert "sn" in result
        assert result["sn"] == "jdoe"

    def test_add_required_attributes_with_names(self) -> None:
        transformer = RecordTransformer()
        record = {"givenname": "John", "sn": "Doe"}
        result = transformer.add_required_attributes(record)

        assert result["cn"] == "John Doe"
        assert result["sn"] == "Doe"

    def test_add_required_attributes_with_displayname(self) -> None:
        transformer = RecordTransformer()
        record = {"displayname": "John Doe"}
        result = transformer.add_required_attributes(record)

        assert result["cn"] == "John Doe"
        assert result["sn"] == "Doe"

    def test_add_required_attributes_existing_objectclass(self) -> None:
        transformer = RecordTransformer()
        record: dict[str, Any] = {"objectclass": ["customClass"], "uid": "jdoe"}
        result = transformer.add_required_attributes(record)

        assert result["objectclass"] == ["customClass"]

    def test_add_required_attributes_multiword_cn(self) -> None:
        transformer = RecordTransformer()
        record = {"cn": "John William Doe"}
        result = transformer.add_required_attributes(record)

        assert result["sn"] == "Doe"

    def test_add_required_attributes_fallback(self) -> None:
        transformer = RecordTransformer()
        record: dict[str, str] = {}
        result = transformer.add_required_attributes(record)

        assert result["cn"] == "Unknown User"
        assert result["sn"] == "User"  # Last word of "Unknown User"
