"""Data validation utilities for LDIF target using flext-ldap infrastructure.

Eliminates code duplication by using LDAP validation functionality from flext-ldap.
"""

from __future__ import annotations

import re

# Use flext-ldap for LDAP-specific validation instead of duplicating
from flext_ldap.utils import (
    flext_ldap_sanitize_attribute_name,
    flext_ldap_validate_attribute_name,
    flext_ldap_validate_attribute_value,
    flext_ldap_validate_dn,
)


class ValidationError(Exception):
    """Error raised when record validation fails."""


def validate_dn_component(value: str) -> bool:
    """Validate a DN component value using flext-ldap infrastructure."""
    if not value:
        return False

    # Use flext-ldap DN validation - no need to duplicate logic
    return flext_ldap_validate_dn(f"test={value}")


def validate_attribute_name(name: str) -> bool:
    """Validate LDAP attribute name using flext-ldap infrastructure."""
    # ELIMINATED DUPLICATION: Use flext-ldap validation instead of local logic
    return flext_ldap_validate_attribute_name(name)


# Constants for validation limits
MAX_ATTRIBUTE_VALUE_LENGTH = 1000


def validate_attribute_value(value: object) -> bool:
    """Validate LDAP attribute value using flext-ldap infrastructure."""
    # ELIMINATED DUPLICATION: Use flext-ldap validation instead of local logic
    # flext_ldap_validate_attribute_value does not accept max_length; enforce locally
    if isinstance(value, str) and len(value) > MAX_ATTRIBUTE_VALUE_LENGTH:
        return False
    return flext_ldap_validate_attribute_value(value)


def sanitize_attribute_name(name: str) -> str:
    """Sanitize field name to be LDAP-compatible using flext-ldap normalization."""
    # Use flext-ldap normalization as base
    normalized = flext_ldap_sanitize_attribute_name(name)

    # Remove invalid characters
    sanitized = re.sub(r"[^a-zA-Z0-9\-]", "", normalized)

    # Ensure starts with letter
    if sanitized and not sanitized[0].isalpha():
        sanitized = "attr" + sanitized

    # Fallback if empty
    if not sanitized:
        sanitized = "unknownAttr"

    return sanitized


def validate_record(record: dict[str, object]) -> dict[str, list[str]]:
    """Validate a record and return validation errors."""
    errors: dict[str, list[str]] = {}

    if not record:
        errors["record"] = ["Record cannot be empty"]
        return errors

    # Check for required fields for DN generation
    has_id_field = any(
        field in record for field in ["id", "uid", "user_id", "username"]
    )

    if not has_id_field:
        errors["dn"] = [
            "Record must contain at least one ID field (id, uid, user_id, or username)",
        ]

    # Validate individual fields
    for field, value in record.items():
        field_errors = []

        # Validate field name
        if not validate_attribute_name(field):
            field_errors.append(f"Invalid attribute name: {field}")

        # Validate field value
        if not validate_attribute_value(value):
            field_errors.append(f"Invalid attribute value for {field}")

        if field_errors:
            errors[field] = field_errors

    return errors


def validate_schema(schema: dict[str, object]) -> dict[str, list[str]]:
    """Validate Singer schema for LDIF compatibility."""
    errors: dict[str, list[str]] = {}

    if not schema:
        errors["schema"] = ["Schema cannot be empty"]
        return errors

    properties = schema.get("properties", {})
    if not properties:
        errors["properties"] = ["Schema must define properties"]
        return errors

    # Ensure properties is a dictionary for type safety
    if not isinstance(properties, dict):
        errors["properties"] = ["Properties must be a dictionary"]
        return errors

    # Check for ID-like fields
    id_fields = [
        field
        for field in properties
        if field.lower() in {"id", "uid", "user_id", "username"}
    ]

    if not id_fields:
        errors["id_fields"] = [
            "Schema should contain at least one ID field for DN generation",
        ]

    # Validate property names
    for prop_name in properties:
        if not validate_attribute_name(prop_name):
            if "invalid_properties" not in errors:
                errors["invalid_properties"] = []
            errors["invalid_properties"].append(f"Invalid property name: {prop_name}")

    return errors
