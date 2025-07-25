"""Configuration utilities for FLEXT Target LDIF - CONSOLIDATED.

Uses flext-meltano common validation to eliminate duplication with tap-ldif.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import typing as t
from pathlib import Path

# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.common import validate_directory_path


def validate_output_path(path: str) -> str:
    """Validate and normalize output path using consolidated patterns."""
    output_path = Path(path)

    # Check if path exists and is a file
    if output_path.exists() and not output_path.is_dir():
        msg = f"Output path '{path}' already exists and is not a directory"
        raise ValueError(msg)

    # Create directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    return str(output_path.absolute())


def validate_dn_template(template: str) -> str:
    """Validate DN template format."""
    if not template:
        msg = "DN template cannot be empty"
        raise ValueError(msg)

    # Basic validation - should contain at least one component
    if "=" not in template:
        msg = f"DN template '{template}' must contain at least one '=' character"
        raise ValueError(msg)

    return template


def get_default_attribute_mapping() -> dict[str, str]:
    """Get default attribute mapping for common fields."""
    return {
        "id": "uid",
        "user_id": "uid",
        "username": "uid",
        "email": "mail",
        "first_name": "givenName",
        "last_name": "sn",
        "full_name": "cn",
        "display_name": "displayName",
        "phone": "telephoneNumber",
        "mobile": "mobile",
        "title": "title",
        "department": "departmentNumber",
        "organization": "o",
        "description": "description",
        "created_at": "createTimestamp",
        "updated_at": "modifyTimestamp",
    }


class ConfigValidationError(Exception):
    """Error raised when configuration validation fails."""


def validate_config(config: dict[str, t.Any]) -> dict[str, t.Any]:
    """Validate and normalize target configuration."""
    validated = config.copy()

    # Validate output path
    if "output_path" in validated:
        validated["output_path"] = validate_output_path(validated["output_path"])

    # Validate DN template
    if "dn_template" in validated:
        validated["dn_template"] = validate_dn_template(validated["dn_template"])

    # Merge with default attribute mapping
    default_mapping = get_default_attribute_mapping()
    user_mapping = validated.get("attribute_mapping", {})
    validated["attribute_mapping"] = {**default_mapping, **user_mapping}

    # Validate LDIF options
    ldif_options = validated.get("ldif_options", {})
    if "line_length" in ldif_options:
        line_length = ldif_options["line_length"]
        if not isinstance(line_length, int) or line_length < 10:
            msg = f"Line length must be an integer >= 10, got {line_length}"
            raise ConfigValidationError(msg)

    return validated
