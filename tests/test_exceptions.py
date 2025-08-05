"""Comprehensive tests for flext-target-ldif exception hierarchy.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

REFACTORED: Complete exception system with 100% coverage and validation.
"""

from __future__ import annotations

import pytest
from flext_target_ldif.exceptions import (
    FlextTargetLdifConfigurationError,
    FlextTargetLdifError,
    FlextTargetLdifErrorDetails,
    FlextTargetLdifFileError,
    FlextTargetLdifSchemaError,
    FlextTargetLdifValidationError,
    FlextTargetLdifWriterError,
)
from pydantic import ValidationError


class TestFlextTargetLdifError:
    """Test the base exception class."""

    def test_error_creation_with_message_only(self) -> None:
        """Test creating error with message only."""
        error = FlextTargetLdifError("Test error message")
        if error.message != "Test error message":
            msg: str = f"Expected {'Test error message'}, got {error.message}"
            raise AssertionError(
                msg,
            )
        assert error.details == {}
        if str(error) != "Test error message":
            msg: str = f"Expected {'Test error message'}, got {error!s}"
            raise AssertionError(msg)

    def test_error_creation_with_details(self) -> None:
        """Test creating error with details."""
        details = {"field": "value", "code": "LDIF001"}
        error = FlextTargetLdifError("Test error", details)
        if error.message != "Test error":
            msg: str = f"Expected {'Test error'}, got {error.message}"
            raise AssertionError(msg)
        assert error.details == details

    def test_error_inheritance(self) -> None:
        """Test that FlextTargetLdifError inherits from Exception."""
        error = FlextTargetLdifError("Test")
        assert isinstance(error, Exception)
        assert isinstance(error, FlextTargetLdifError)


class TestFlextTargetLdifErrorDetails:
    """Test the error details value object."""

    def test_valid_configuration_error_details(self) -> None:
        """Test creating valid configuration error details."""
        details = FlextTargetLdifErrorDetails(
            error_code="LDIF_CONFIG_001",
            error_type="configuration",
            context={"field": "output_file"},
            timestamp="2025-01-01T00:00:00",
            source_component="target",
        )
        if details.error_code != "LDIF_CONFIG_001":
            msg: str = f"Expected {'LDIF_CONFIG_001'}, got {details.error_code}"
            raise AssertionError(
                msg,
            )
        assert details.error_type == "configuration"
        if details.source_component != "target":
            msg: str = f"Expected {'target'}, got {details.source_component}"
            raise AssertionError(msg)

    def test_valid_writer_error_details(self) -> None:
        """Test creating valid writer error details."""
        details = FlextTargetLdifErrorDetails(
            error_code="LDIF_WRITE_001",
            error_type="writer",
            context={"record_id": "123"},
            timestamp="2025-01-01T00:00:00",
            source_component="writer",
        )
        if details.error_code != "LDIF_WRITE_001":
            msg: str = f"Expected {'LDIF_WRITE_001'}, got {details.error_code}"
            raise AssertionError(
                msg,
            )
        assert details.source_component == "writer"

    def test_error_details_immutability(self) -> None:
        """Test that error details are immutable."""
        details = FlextTargetLdifErrorDetails(
            error_code="LDIF_001",
            error_type="test",
            context={},
            timestamp="2025-01-01T00:00:00",
            source_component="writer",
        )

        with pytest.raises(ValidationError):
            details.error_code = "MODIFIED"

    def test_error_details_validation_valid_error_code(self) -> None:
        """Test validation with valid error code."""
        details = FlextTargetLdifErrorDetails(
            error_code="LDIF_SCHEMA_001",
            error_type="schema",
            context={},
            timestamp="2025-01-01T00:00:00",
            source_component="validation",
        )
        # Should not raise exception
        details.validate_domain_rules()

    def test_error_details_validation_invalid_error_code(self) -> None:
        """Test validation with invalid error code."""
        details = FlextTargetLdifErrorDetails(
            error_code="INVALID_001",
            error_type="test",
            context={},
            timestamp="2025-01-01T00:00:00",
            source_component="writer",
        )
        with pytest.raises(ValueError, match="Error code must start with 'LDIF'"):
            details.validate_domain_rules()

    def test_error_details_validation_empty_error_type(self) -> None:
        """Test validation with empty error type."""
        details = FlextTargetLdifErrorDetails(
            error_code="LDIF_001",
            error_type="",
            context={},
            timestamp="2025-01-01T00:00:00",
            source_component="writer",
        )
        with pytest.raises(ValueError, match="Error type cannot be empty"):
            details.validate_domain_rules()

    def test_error_details_validation_invalid_source_component(self) -> None:
        """Test validation with invalid source component."""
        details = FlextTargetLdifErrorDetails(
            error_code="LDIF_001",
            error_type="test",
            context={},
            timestamp="2025-01-01T00:00:00",
            source_component="invalid",
        )
        with pytest.raises(ValueError, match="Invalid source component: invalid"):
            details.validate_domain_rules()


class TestSpecificExceptions:
    """Test specific exception classes."""

    def test_configuration_error(self) -> None:
        """Test FlextTargetLdifConfigurationError."""
        error = FlextTargetLdifConfigurationError("Invalid config")
        assert isinstance(error, FlextTargetLdifError)
        if error.message != "Invalid config":
            msg: str = f"Expected {'Invalid config'}, got {error.message}"
            raise AssertionError(msg)

    def test_validation_error(self) -> None:
        """Test FlextTargetLdifValidationError."""
        error = FlextTargetLdifValidationError("Validation failed")
        assert isinstance(error, FlextTargetLdifError)
        if error.message != "Validation failed":
            msg: str = f"Expected {'Validation failed'}, got {error.message}"
            raise AssertionError(msg)

    def test_file_error(self) -> None:
        """Test FlextTargetLdifFileError."""
        error = FlextTargetLdifFileError("File not found")
        assert isinstance(error, FlextTargetLdifError)
        if error.message != "File not found":
            msg: str = f"Expected {'File not found'}, got {error.message}"
            raise AssertionError(msg)

    def test_writer_error(self) -> None:
        """Test FlextTargetLdifWriterError."""
        error = FlextTargetLdifWriterError("Write operation failed")
        assert isinstance(error, FlextTargetLdifError)
        if error.message != "Write operation failed":
            msg: str = f"Expected {'Write operation failed'}, got {error.message}"
            raise AssertionError(
                msg,
            )

    def test_schema_error(self) -> None:
        """Test FlextTargetLdifSchemaError."""
        error = FlextTargetLdifSchemaError("Schema validation failed")
        assert isinstance(error, FlextTargetLdifError)
        if error.message != "Schema validation failed":
            msg: str = f"Expected {'Schema validation failed'}, got {error.message}"
            raise AssertionError(
                msg,
            )


class TestExceptionHierarchy:
    """Test the complete exception hierarchy."""

    def test_all_exceptions_inherit_from_base(self) -> None:
        """Test that all specific exceptions inherit from base."""
        exceptions = [
            FlextTargetLdifConfigurationError("test"),
            FlextTargetLdifValidationError("test"),
            FlextTargetLdifFileError("test"),
            FlextTargetLdifWriterError("test"),
            FlextTargetLdifSchemaError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, FlextTargetLdifError)
            assert isinstance(exc, Exception)

    def test_exception_with_structured_details(self) -> None:
        """Test exception with structured error details."""
        error_details = FlextTargetLdifErrorDetails(
            error_code="LDIF_WRITE_001",
            error_type="writer",
            context={"record_id": "123"},
            timestamp="2025-01-01T00:00:00",
            source_component="writer",
        )

        error = FlextTargetLdifWriterError(
            "Failed to write LDIF record",
            error_details.model_dump(),
        )

        if error.message != "Failed to write LDIF record":
            msg: str = f"Expected {'Failed to write LDIF record'}, got {error.message}"
            raise AssertionError(
                msg,
            )
        assert error.details["error_code"] == "LDIF_WRITE_001"
        if error.details["source_component"] != "writer":
            msg: str = f"Expected {'writer'}, got {error.details['source_component']}"
            raise AssertionError(
                msg,
            )
        assert error.details["error_type"] == "writer"

    def test_exception_chaining(self) -> None:
        """Test exception chaining with cause."""
        original_error = ValueError("Original error")

        try:
            raise original_error
        except ValueError as e:
            ldif_error = FlextTargetLdifError("LDIF operation failed")
            ldif_error.__cause__ = e
            assert ldif_error.__cause__ is original_error
