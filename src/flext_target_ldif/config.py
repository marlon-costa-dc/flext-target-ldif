"""Configuration classes for FLEXT Target LDIF using flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextModels, FlextResult

# Use flext-ldap for DN validation - no duplication
from flext_ldap.utils import flext_ldap_validate_dn
from pydantic import Field, field_validator


class FlextTargetLdifConfig(FlextModels.BaseConfig):
    """Configuration for FLEXT Target LDIF using FlextConfig.BaseModel patterns."""

    output_path: str = Field(
        default="./output",
        description="Directory path for LDIF output files",
    )
    file_naming_pattern: str = Field(
        default="{stream_name}_{timestamp}.ldif",
        description="Pattern for LDIF file names. Available variables: {stream_name}, {timestamp}",
    )
    dn_template: str = Field(
        description="Template for generating Distinguished Names (DN) - MUST be configured for production",
        json_schema_extra={"example": "uid={uid},ou=users,dc=company,dc=local"},
    )
    attribute_mapping: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of stream fields to LDAP attributes",
    )
    ldif_options: dict[str, object] = Field(
        default_factory=lambda: dict[str, object](
            {
                "line_length": 78,
                "base64_encode": False,
                "include_timestamps": True,
            },
        ),
        description="LDIF format options",
    )

    @field_validator("output_path")
    @classmethod
    def validate_output_path(cls, v: str) -> str:
        """Validate output path exists or can be created."""
        if not v:
            msg = "Output path cannot be empty"
            raise ValueError(msg)

        path = Path(v)
        try:
            path.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            error_msg: str = f"Cannot create output directory: {e}"
            raise ValueError(error_msg) from e

        return v

    @field_validator("dn_template")
    @classmethod
    def validate_dn_template(cls, v: str) -> str:
        """Validate DN template has proper format."""
        if not v:
            msg = "DN template cannot be empty"
            raise ValueError(msg)

        if "{" not in v or "}" not in v:
            msg = "DN template must contain at least one variable placeholder"
            raise ValueError(msg)

        return v

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate LDIF target configuration business rules using FlextModels.BaseConfig pattern."""
        try:
            # Validate output path is accessible
            output_path = Path(self.output_path)
            if not output_path.exists():
                try:
                    output_path.mkdir(parents=True, exist_ok=True)
                except (OSError, PermissionError) as e:
                    return FlextResult[None].fail(f"Cannot access output path: {e}")

            # Use flext-ldap for DN validation - NO local duplication
            if not self.dn_template:
                return FlextResult[None].fail("DN template cannot be empty")

            # For template validation, create a sample DN with dummy values
            sample_dn = self.dn_template.replace("{uid}", "testuser").replace(
                "{cn}",
                "Test User",
            )
            if not flext_ldap_validate_dn(sample_dn):
                return FlextResult[None].fail(
                    "DN template format is invalid - must follow LDAP DN structure",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Configuration validation failed: {e}")


__all__: list[str] = [
    "FlextTargetLdifConfig",
]
