"""LDIF target exception hierarchy using flext-core patterns."""

from __future__ import annotations

from typing import Any

from flext_core import FlextValueObject


class FlextTargetLdifError(Exception):
    """Base exception for FlextTargetLdif."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize exception with message and optional details."""
        super().__init__(message)
        self.message = message
        self.details = details or {}


class FlextTargetLdifConnectionError(FlextTargetLdifError):
    """Connection-related errors."""


class FlextTargetLdifAuthenticationError(FlextTargetLdifError):
    """Authentication-related errors."""


class FlextTargetLdifValidationError(FlextTargetLdifError):
    """Validation-related errors."""


class FlextTargetLdifTransformationError(FlextTargetLdifError):
    """Data transformation errors."""


class FlextTargetLdifProcessingError(FlextTargetLdifError):
    """Record processing errors."""


class FlextTargetLdifConfigurationError(FlextTargetLdifError):
    """Configuration-related errors."""


class FlextTargetLdifInfrastructureError(FlextTargetLdifError):
    """Infrastructure and dependency injection errors."""


class FlextTargetLdifWriterError(FlextTargetLdifError):
    """LDIF writer-specific errors."""


class FlextTargetLdifFileError(FlextTargetLdifError):
    """File-related errors."""


class FlextTargetLdifSchemaError(FlextTargetLdifError):
    """Schema validation errors."""


class FlextTargetLdifErrorDetails(FlextValueObject):
    """Structured error details using flext-core patterns."""

    error_code: str
    error_type: str
    context: dict[str, Any]
    timestamp: str
    source_component: str

    def validate_domain_rules(self) -> None:
        """Validate domain-specific business rules."""
        # Validate error code format
        if not self.error_code or not self.error_code.startswith("LDIF"):
            msg = "Error code must start with 'LDIF'"
            raise ValueError(msg)

        # Validate error type is not empty
        if not self.error_type:
            msg = "Error type cannot be empty"
            raise ValueError(msg)

        # Validate source component is valid
        valid_components = ["writer", "sinks", "target", "infrastructure", "validation"]
        if self.source_component not in valid_components:
            msg = f"Invalid source component: {self.source_component}"
            raise ValueError(msg)
