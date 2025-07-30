"""LDIF target exception hierarchy using flext-core patterns."""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult, FlextValueObject
from flext_core.exceptions import (
    FlextAuthenticationError,
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextProcessingError,
    FlextValidationError,
)


class FlextTargetLdifError(FlextError):
    """Base exception for FlextTargetLdif."""

    def __init__(
        self,
        message: str = "LDIF target error",
        details: dict[str, Any] | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize exception with message and optional details."""
        context = kwargs.copy()
        if details:
            context.update(details)

        super().__init__(message, error_code="LDIF_TARGET_ERROR", context=context)


class FlextTargetLdifConnectionError(FlextConnectionError):
    """Connection-related errors."""

    def __init__(
        self,
        message: str = "LDIF target connection failed",
        host: str | None = None,
        port: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target connection error with context."""
        context = kwargs.copy()
        if host is not None:
            context["host"] = host
        if port is not None:
            context["port"] = port

        super().__init__(f"LDIF target connection: {message}", **context)


class FlextTargetLdifAuthenticationError(FlextAuthenticationError):
    """Authentication-related errors."""

    def __init__(
        self,
        message: str = "LDIF target authentication failed",
        auth_method: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target authentication error with context."""
        context = kwargs.copy()
        if auth_method is not None:
            context["auth_method"] = auth_method

        super().__init__(f"LDIF target auth: {message}", **context)


class FlextTargetLdifValidationError(FlextValidationError):
    """Validation-related errors."""

    def __init__(
        self,
        message: str = "LDIF target validation failed",
        field: str | None = None,
        value: object = None,
        record_number: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target validation error with context."""
        validation_details = {}
        if field is not None:
            validation_details["field"] = field
        if value is not None:
            validation_details["value"] = str(value)[:100]  # Truncate long values

        context = kwargs.copy()
        if record_number is not None:
            context["record_number"] = record_number

        super().__init__(
            f"LDIF target validation: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextTargetLdifTransformationError(FlextProcessingError):
    """Data transformation errors."""

    def __init__(
        self,
        message: str = "LDIF target transformation failed",
        record_data: dict[str, Any] | None = None,
        transformation_stage: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target transformation error with context."""
        context = kwargs.copy()
        if record_data is not None:
            # Include minimal record info for debugging
            context["record_keys"] = list(record_data.keys())
        if transformation_stage is not None:
            context["transformation_stage"] = transformation_stage

        super().__init__(f"LDIF target transformation: {message}", **context)


class FlextTargetLdifProcessingError(FlextProcessingError):
    """Record processing errors."""

    def __init__(
        self,
        message: str = "LDIF target processing failed",
        record_number: int | None = None,
        processing_stage: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target processing error with context."""
        context = kwargs.copy()
        if record_number is not None:
            context["record_number"] = record_number
        if processing_stage is not None:
            context["processing_stage"] = processing_stage

        super().__init__(f"LDIF target processing: {message}", **context)


class FlextTargetLdifConfigurationError(FlextConfigurationError):
    """Configuration-related errors."""

    def __init__(
        self,
        message: str = "LDIF target configuration error",
        config_key: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target configuration error with context."""
        context = kwargs.copy()
        if config_key is not None:
            context["config_key"] = config_key

        super().__init__(f"LDIF target config: {message}", **context)


class FlextTargetLdifInfrastructureError(FlextTargetLdifError):
    """Infrastructure and dependency injection errors."""

    def __init__(
        self,
        message: str = "LDIF target infrastructure error",
        component: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target infrastructure error with context."""
        context = kwargs.copy()
        if component is not None:
            context["component"] = component

        super().__init__(f"LDIF target infrastructure: {message}", **context)


class FlextTargetLdifWriterError(FlextTargetLdifError):
    """LDIF writer-specific errors."""

    def __init__(
        self,
        message: str = "LDIF writer error",
        output_file: str | None = None,
        line_number: int | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF writer error with context."""
        context = kwargs.copy()
        if output_file is not None:
            context["output_file"] = output_file
        if line_number is not None:
            context["line_number"] = line_number

        super().__init__(f"LDIF writer: {message}", **context)


class FlextTargetLdifFileError(FlextTargetLdifError):
    """File-related errors."""

    def __init__(
        self,
        message: str = "LDIF target file error",
        file_path: str | None = None,
        operation: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target file error with context."""
        context = kwargs.copy()
        if file_path is not None:
            context["file_path"] = file_path
        if operation is not None:
            context["operation"] = operation

        super().__init__(f"LDIF target file: {message}", **context)


class FlextTargetLdifSchemaError(FlextValidationError):
    """Schema validation errors."""

    def __init__(
        self,
        message: str = "LDIF target schema validation failed",
        schema_name: str | None = None,
        field: str | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize LDIF target schema error with context."""
        validation_details = {}
        if field is not None:
            validation_details["field"] = field

        context = kwargs.copy()
        if schema_name is not None:
            context["schema_name"] = schema_name

        super().__init__(
            f"LDIF target schema: {message}",
            validation_details=validation_details,
            context=context,
        )


class FlextTargetLdifErrorDetails(FlextValueObject):
    """Structured error details using flext-core patterns."""

    error_code: str
    error_type: str
    context: dict[str, Any]
    timestamp: str
    source_component: str

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate domain-specific business rules."""
        try:
            # Validate error code format
            if not self.error_code or not self.error_code.startswith("LDIF"):
                return FlextResult.fail("Error code must start with 'LDIF'")

            # Validate error type is not empty
            if not self.error_type:
                return FlextResult.fail("Error type cannot be empty")

            # Validate source component is valid
            valid_components = [
                "writer",
                "sinks",
                "target",
                "infrastructure",
                "validation",
            ]
            if self.source_component not in valid_components:
                return FlextResult.fail(
                    f"Invalid source component: {self.source_component}",
                )

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Domain validation failed: {e}")
