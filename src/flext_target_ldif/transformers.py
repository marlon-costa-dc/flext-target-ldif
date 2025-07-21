"""Data transformation utilities for LDIF target."""

from __future__ import annotations

import typing as t
from datetime import datetime


def transform_timestamp(value: t.Any) -> str:
    """Transform timestamp values to LDAP timestamp format."""
    if value is None:
        return ""

    if isinstance(value, datetime):
        # LDAP GeneralizedTime format: YYYYMMDDHHMMSSZ
        return value.strftime("%Y%m%d%H%M%SZ")

    if isinstance(value, str):
        try:
            # Try to parse ISO format
            dt = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
            return dt.strftime("%Y%m%d%H%M%SZ")
        except ValueError:
            # Return as-is if not parseable
            return value

    return str(value)


def transform_boolean(value: t.Any) -> str:
    """Transform boolean values to LDAP boolean format."""
    if value is None:
        return ""

    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    if isinstance(value, str):
        lower_val = value.lower()
        if lower_val in {"true", "yes", "1", "on"}:
            return "TRUE"
        if lower_val in {"false", "no", "0", "off"}:
            return "FALSE"

    return str(value)


def transform_email(value: t.Any) -> str:
    """Transform email values to ensure LDAP compatibility."""
    if value is None:
        return ""

    email_str = str(value).strip().lower()

    # Basic email validation and cleanup
    if "@" in email_str and "." in email_str:
        return email_str

    return ""


def transform_phone(value: t.Any) -> str:
    """Transform phone numbers to standard format."""
    if value is None:
        return ""

    phone_str = str(value)

    # Remove common formatting characters
    return "".join(c for c in phone_str if c.isdigit() or c in "+- ()")


def transform_name(value: t.Any) -> str:
    """Transform name fields to ensure proper formatting."""
    if value is None:
        return ""

    name_str = str(value).strip()

    # Capitalize first letter of each word
    return " ".join(word.capitalize() for word in name_str.split())


def normalize_attribute_value(
    attr_name: str,
    value: t.Any,
    transformers: dict[str, t.Callable[[t.Any], str]] | None = None,
) -> str:
    """Normalize attribute value based on attribute type."""
    if value is None:
        return ""

    # Use custom transformers if provided
    if transformers and attr_name in transformers:
        return transformers[attr_name](value)

    # Built-in transformations based on attribute name
    attr_lower = attr_name.lower()

    if attr_lower in {"mail", "email"}:
        return transform_email(value)
    if attr_lower in {"telephonenumber", "phone", "mobile"}:
        return transform_phone(value)
    if attr_lower in {"givenname", "sn", "cn", "displayname"}:
        return transform_name(value)
    if attr_lower in {"createtimestamp", "modifytimestamp"}:
        return transform_timestamp(value)
    if attr_lower.endswith("boolean") or attr_lower.startswith("is"):
        return transform_boolean(value)
    # Default: convert to string and strip whitespace
    return str(value).strip()


class RecordTransformer:
    """Transform Singer records for LDIF output."""

    def __init__(
        self,
        attribute_mapping: dict[str, str] | None = None,
        custom_transformers: dict[str, t.Callable[[t.Any], str]] | None = None,
    ) -> None:
        """Initialize the record transformer."""
        self.attribute_mapping = attribute_mapping or {}
        self.custom_transformers = custom_transformers or {}

    def transform_record(self, record: dict[str, t.Any]) -> dict[str, str]:
        """Transform a Singer record to LDAP-compatible format."""
        transformed = {}

        for field, value in record.items():
            # Skip None values
            if value is None:
                continue

            # Map field name if needed
            if field in self.attribute_mapping:
                attr_name = self.attribute_mapping[field]
            else:
                # Default mapping: convert to lowercase, remove underscores
                attr_name = field.lower().replace("_", "")

            # Transform value
            transformed_value = normalize_attribute_value(
                attr_name,
                value,
                self.custom_transformers,
            )

            # Only include non-empty values
            if transformed_value:
                transformed[attr_name] = transformed_value

        return transformed

    def add_required_attributes(self, record: dict[str, str]) -> dict[str, t.Any]:
        """Add required LDAP attributes to the record."""
        result: dict[str, t.Any] = record.copy()

        # Ensure objectClass is present
        if "objectclass" not in result:
            result["objectclass"] = ["inetOrgPerson", "person"]

        # Ensure cn (common name) is present
        if "cn" not in result:
            # Try to build from other name fields
            if "givenname" in result and "sn" in result:
                result["cn"] = f"{result['givenname']} {result['sn']}"
            elif "displayname" in result:
                result["cn"] = result["displayname"]
            elif "uid" in result:
                result["cn"] = result["uid"]
            else:
                result["cn"] = "Unknown User"

        # Ensure sn (surname) is present for person objectClass
        if "sn" not in result:
            if "cn" in result:
                # Use last word of cn as surname
                words = result["cn"].split()
                result["sn"] = words[-1] if words else "Unknown"
            else:
                result["sn"] = "Unknown"

        return result
