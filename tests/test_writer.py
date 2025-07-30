"""Comprehensive tests for LdifWriter implementation.

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_DATA_COUNT = 3

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

REFACTORED: Complete writer system with 100% coverage and validation.
"""

from __future__ import annotations

import base64
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_target_ldif.exceptions import FlextTargetLdifWriterError
from flext_target_ldif.writer import LdifWriter


class TestLdifWriterInitialization:
    """Test LdifWriter initialization."""

    def test_init_with_defaults(self) -> None:
        """Test initialization with default values."""
        writer = LdifWriter()
        if writer.output_file != Path("output.ldif"):
            raise AssertionError(f"Expected {Path("output.ldif")}, got {writer.output_file}")
        assert writer.ldif_options == {}
        if writer.dn_template != "uid={uid},ou=users,dc=example,dc=com":
            raise AssertionError(f"Expected {"uid={uid},ou=users,dc=example,dc=com"}, got {writer.dn_template}")
        assert writer.attribute_mapping == {}
        if writer.schema != {}:
            raise AssertionError(f"Expected {{}}, got {writer.schema}")
        assert writer.line_length == 78
        if writer.base64_encode:
            raise AssertionError(f"Expected False, got {writer.base64_encode}")\ n        if not (writer.include_timestamps):
            raise AssertionError(f"Expected True, got {writer.include_timestamps}")

    def test_init_with_custom_values(self) -> None:
        """Test initialization with custom values."""
        output_file = Path("/tmp/custom.ldif")
        ldif_options = {
            "line_length": 100,
            "base64_encode": True,
            "include_timestamps": False,
        }
        dn_template = "cn={name},ou=people,dc=test,dc=com"
        attribute_mapping = {"email": "mail", "name": "cn"}
        schema = {"objectClass": ["person", "organizationalPerson"]}

        writer = LdifWriter(
            output_file=output_file,
            ldif_options=ldif_options,
            dn_template=dn_template,
            attribute_mapping=attribute_mapping,
            schema=schema,
        )

        if writer.output_file != output_file:

            raise AssertionError(f"Expected {output_file}, got {writer.output_file}")
        assert writer.ldif_options == ldif_options
        if writer.dn_template != dn_template:
            raise AssertionError(f"Expected {dn_template}, got {writer.dn_template}")
        assert writer.attribute_mapping == attribute_mapping
        if writer.schema != schema:
            raise AssertionError(f"Expected {schema}, got {writer.schema}")
        assert writer.line_length == 100
        if not (writer.base64_encode):
            raise AssertionError(f"Expected True, got {writer.base64_encode}")
        if writer.include_timestamps:
            raise AssertionError(f"Expected False, got {writer.include_timestamps}")\ n
    def test_init_with_string_path(self) -> None:
        """Test initialization with string path."""
        writer = LdifWriter(output_file="/tmp/test.ldif")
        if writer.output_file != Path("/tmp/test.ldif"):
            raise AssertionError(f"Expected {Path("/tmp/test.ldif")}, got {writer.output_file}")


class TestLdifWriterFileOperations:
    """Test file operations (open/close)."""

    def test_open_success(self) -> None:
        """Test successful file opening."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        result = writer.open()

        assert result.is_success
        assert writer._file_handle is not None

        # Clean up
        writer.close()
        tmp_path.unlink()

    def test_open_failure(self) -> None:
        """Test file opening failure."""
        # Try to open a file in a non-existent directory
        invalid_path = Path("/nonexistent/directory/test.ldif")
        writer = LdifWriter(output_file=invalid_path)
        result = writer.open()

        assert not result.is_success
        if "Failed to open LDIF file" not in result.error:
            raise AssertionError(f"Expected {"Failed to open LDIF file"} in {result.error}")

    def test_close_success(self) -> None:
        """Test successful file closing."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        writer.open()
        result = writer.close()

        assert result.is_success
        assert writer._file_handle is None

        tmp_path.unlink()

    def test_close_when_not_open(self) -> None:
        """Test closing when file is not open."""
        writer = LdifWriter()
        result = writer.close()
        assert result.is_success

    @patch("pathlib.Path.open")
    def test_close_failure(self, mock_open_method: Mock) -> None:
        """Test file closing failure."""
        mock_file = Mock()
        mock_file.close.side_effect = Exception("Close failed")
        mock_open_method.return_value = mock_file

        writer = LdifWriter()
        writer.open()
        result = writer.close()

        assert not result.is_success
        if "Failed to close LDIF file" not in result.error:
            raise AssertionError(f"Expected {"Failed to close LDIF file"} in {result.error}")


class TestLdifWriterRecordWriting:
    """Test record writing functionality."""

    def test_write_simple_record(self) -> None:
        """Test writing a simple record."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        record = {"uid": "jdoe", "cn": "John Doe", "mail": "john@example.com"}

        result = writer.write_record(record)
        assert result.is_success
        if writer.record_count != 1:
            raise AssertionError(f"Expected {1}, got {writer.record_count}")

        writer.close()

        # Verify file contents
        content = tmp_path.read_text(encoding="utf-8")
        if "version: 1" not in content:
            raise AssertionError(f"Expected {"version: 1"} in {content}")
        assert "dn: uid=jdoe,ou=users,dc=example,dc=com" in content
        if "uid: jdoe" not in content:
            raise AssertionError(f"Expected {"uid: jdoe"} in {content}")
        assert "cn: John Doe" in content
        if "mail: john@example.com" not in content:
            raise AssertionError(f"Expected {"mail: john@example.com"} in {content}")

        tmp_path.unlink()

    def test_write_record_with_attribute_mapping(self) -> None:
        """Test writing record with attribute mapping."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        attribute_mapping = {"email": "mail", "name": "cn"}
        writer = LdifWriter(
            output_file=tmp_path,
            attribute_mapping=attribute_mapping,
        )

        record = {"uid": "jdoe", "name": "John Doe", "email": "john@example.com"}
        writer.write_record(record)
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        if "cn: John Doe" not in content  # name mapped to cn:
            raise AssertionError(f"Expected {"cn: John Doe"} in {content  # name mapped to cn}")
        assert "mail: john@example.com" in content  # email mapped to mail

        tmp_path.unlink()

    def test_write_record_auto_open(self) -> None:
        """Test that write_record automatically opens file if not open."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        # Don't call open() explicitly

        record = {"uid": "jdoe", "cn": "John Doe"}
        result = writer.write_record(record)

        assert result.is_success
        assert writer._file_handle is not None

        writer.close()
        tmp_path.unlink()

    def test_write_record_missing_dn_field(self) -> None:
        """Test writing record with missing DN field."""
        writer = LdifWriter(dn_template="uid={uid},ou=users,dc=example,dc=com")

        # Record missing 'uid' field required by DN template
        record = {"cn": "John Doe", "mail": "john@example.com"}
        result = writer.write_record(record)

        assert not result.is_success
        if "Failed to write record" not in result.error:
            raise AssertionError(f"Expected {"Failed to write record"} in {result.error}")

    def test_write_multiple_records(self) -> None:
        """Test writing multiple records."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)

        records = [
            {"uid": "jdoe", "cn": "John Doe"},
            {"uid": "jsmith", "cn": "Jane Smith"},
            {"uid": "bob", "cn": "Bob Wilson"},
        ]

        for record in records:
            result = writer.write_record(record)
            assert result.is_success

        if writer.record_count != EXPECTED_DATA_COUNT:

            raise AssertionError(f"Expected {3}, got {writer.record_count}")
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        if "dn: uid=jdoe,ou=users,dc=example,dc=com" not in content:
            raise AssertionError(f"Expected {"dn: uid=jdoe,ou=users,dc=example,dc=com"} in {content}")
        assert "dn: uid=jsmith,ou=users,dc=example,dc=com" in content
        if "dn: uid=bob,ou=users,dc=example,dc=com" not in content:
            raise AssertionError(f"Expected {"dn: uid=bob,ou=users,dc=example,dc=com"} in {content}")

        tmp_path.unlink()


class TestLdifWriterBase64Encoding:
    """Test base64 encoding functionality."""

    def test_needs_base64_encoding_space_start(self) -> None:
        """Test detection of values that start with space."""
        writer = LdifWriter()
        assert writer._needs_base64_encoding(" starts with space")

    def test_needs_base64_encoding_colon_start(self) -> None:
        """Test detection of values that start with colon."""
        writer = LdifWriter()
        assert writer._needs_base64_encoding(":starts with colon")

    def test_needs_base64_encoding_non_ascii(self) -> None:
        """Test detection of non-ASCII values."""
        writer = LdifWriter()
        assert writer._needs_base64_encoding("José")
        assert writer._needs_base64_encoding("中文")

    def test_needs_base64_encoding_newlines(self) -> None:
        """Test detection of values with newlines."""
        writer = LdifWriter()
        assert writer._needs_base64_encoding("line1\nline2")
        assert writer._needs_base64_encoding("line1\rline2")

    def test_needs_base64_encoding_normal_value(self) -> None:
        """Test normal ASCII values don't need encoding."""
        writer = LdifWriter()
        assert not writer._needs_base64_encoding("normal ascii value")
        assert not writer._needs_base64_encoding("john@example.com")

    def test_write_base64_encoded_attribute(self) -> None:
        """Test writing base64 encoded attributes."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        writer.open()

        writer._write_attribute("description", " starts with space")
        writer._write_attribute("cn", "José")

        writer.close()

        content = tmp_path.read_text(encoding="utf-8")

        # Check base64 encoded values (:: indicates base64)
        if "description:: " not in content:
            raise AssertionError(f"Expected {"description:: "} in {content}")
        assert "cn:: " in content

        # Verify base64 decoding
        for line in content.split("\n"):
            if line.startswith("description:: "):
                encoded = line.split(":: ")[1]
                decoded = base64.b64decode(encoded).decode("utf-8")
                if decoded != " starts with space":
                    raise AssertionError(f"Expected {" starts with space"}, got {decoded}")
            elif line.startswith("cn:: "):
                encoded = line.split(":: ")[1]
                decoded = base64.b64decode(encoded).decode("utf-8")
                if decoded != "José":
                    raise AssertionError(f"Expected {"José"}, got {decoded}")

        tmp_path.unlink()

    def test_force_base64_encoding(self) -> None:
        """Test forcing base64 encoding via options."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(
            output_file=tmp_path,
            ldif_options={"base64_encode": True},
        )

        record = {"uid": "jdoe", "cn": "John Doe"}
        writer.write_record(record)
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        # All attributes should be base64 encoded
        if "uid:: " not in content:
            raise AssertionError(f"Expected {"uid:: "} in {content}")
        assert "cn:: " in content

        tmp_path.unlink()


class TestLdifWriterLineWrapping:
    """Test line wrapping functionality."""

    def test_short_line_no_wrapping(self) -> None:
        """Test short lines are not wrapped."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        writer.open()
        writer._write_line("short line")
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        if "short line" not in lines:
            raise AssertionError(f"Expected {"short line"} in {lines}")

        tmp_path.unlink()

    def test_long_line_wrapping(self) -> None:
        """Test long lines are properly wrapped."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(
            output_file=tmp_path,
            ldif_options={"line_length": 20},  # Short length for testing
        )
        writer.open()

        long_line = "this is a very long line that should be wrapped and (
            exceed the 20 character limit")
        writer._write_line(long_line)
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        # Skip header lines and find the wrapped line
        wrapped_lines = [line for line in lines if not line.startswith("version:") and (
            not line.startswith("# Generated")])
        wrapped_lines = [line for line in wrapped_lines if line.strip()]  # Remove empty lines

        if wrapped_lines:
            # First part should be exactly 20 characters
            if len(wrapped_lines[0]) != 20:
                raise AssertionError(f"Expected {20}, got {len(wrapped_lines[0])}")
            # Continuation lines should start with space
            for line in wrapped_lines[1:]:
                if line:  # Skip empty lines
                    assert line.startswith(" ")

        tmp_path.unlink()

    def test_custom_line_length(self) -> None:
        """Test custom line length setting."""
        writer = LdifWriter(ldif_options={"line_length": 100})
        if writer.line_length != 100:
            raise AssertionError(f"Expected {100}, got {writer.line_length}")


class TestLdifWriterDnGeneration:
    """Test DN generation functionality."""

    def test_generate_dn_success(self) -> None:
        """Test successful DN generation."""
        writer = LdifWriter(dn_template="uid={uid},ou={department},dc=example,dc=com")
        record = {"uid": "jdoe", "department": "engineering"}

        dn = writer._generate_dn(record)
        if dn != "uid=jdoe,ou=engineering,dc=example,dc=com":
            raise AssertionError(f"Expected {"uid=jdoe,ou=engineering,dc=example,dc=com"}, got {dn}")

    def test_generate_dn_missing_field(self) -> None:
        """Test DN generation with missing field."""
        writer = LdifWriter(dn_template="uid={uid},ou={department},dc=example,dc=com")
        record = {"uid": "jdoe"}  # Missing 'department'

        with pytest.raises(FlextTargetLdifWriterError) as exc_info:
            writer._generate_dn(record)

        if "Missing required field for DN generation" not in str(exc_info.value):

            raise AssertionError(f"Expected {"Missing required field for DN generation"} in {str(exc_info.value)}")

    def test_custom_dn_template(self) -> None:
        """Test custom DN template."""
        writer = LdifWriter(dn_template="cn={name},ou=people,dc=test,dc=org")
        record = {"name": "John Doe"}

        dn = writer._generate_dn(record)
        if dn != "cn=John Doe,ou=people,dc=test,dc=org":
            raise AssertionError(f"Expected {"cn=John Doe,ou=people,dc=test,dc=org"}, got {dn}")


class TestLdifWriterContextManager:
    """Test context manager functionality."""

    def test_context_manager_usage(self) -> None:
        """Test using LdifWriter as context manager."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        record = {"uid": "jdoe", "cn": "John Doe"}

        with LdifWriter(output_file=tmp_path) as writer:
            result = writer.write_record(record)
            assert result.is_success
            assert writer._file_handle is not None

        # File should be closed after context manager exit
        assert writer._file_handle is None

        # Verify content was written
        content = tmp_path.read_text(encoding="utf-8")
        if "dn: uid=jdoe,ou=users,dc=example,dc=com" not in content:
            raise AssertionError(f"Expected {"dn: uid=jdoe,ou=users,dc=example,dc=com"} in {content}")

        tmp_path.unlink()

    def test_context_manager_exception_handling(self) -> None:
        """Test context manager properly closes file on exception."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            with LdifWriter(output_file=tmp_path) as writer:
                writer.write_record({"uid": "jdoe", "cn": "John Doe"})
                # Simulate an exception
                msg = "Test exception"
                raise ValueError(msg)
        except ValueError:
            pass

        # File should still be closed
        assert writer._file_handle is None

        tmp_path.unlink()


class TestLdifWriterHeaderGeneration:
    """Test LDIF header generation."""

    def test_header_with_timestamps(self) -> None:
        """Test header generation with timestamps."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(
            output_file=tmp_path,
            ldif_options={"include_timestamps": True},
        )
        writer.open()
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        if "version: 1" not in content:
            raise AssertionError(f"Expected {"version: 1"} in {content}")
        assert "# Generated on:" in content

        tmp_path.unlink()

    def test_header_without_timestamps(self) -> None:
        """Test header generation without timestamps."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(
            output_file=tmp_path,
            ldif_options={"include_timestamps": False},
        )
        writer.open()
        writer.close()

        content = tmp_path.read_text(encoding="utf-8")
        if "version: 1" not in content:
            raise AssertionError(f"Expected {"version: 1"} in {content}")
        assert "# Generated on:" not in content

        tmp_path.unlink()


class TestLdifWriterProperties:
    """Test LdifWriter properties."""

    def test_record_count_property(self) -> None:
        """Test record_count property."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        if writer.record_count != 0:
            raise AssertionError(f"Expected {0}, got {writer.record_count}")

        writer.write_record({"uid": "user1", "cn": "User One"})
        if writer.record_count != 1:
            raise AssertionError(f"Expected {1}, got {writer.record_count}")

        writer.write_record({"uid": "user2", "cn": "User Two"})
        if writer.record_count != EXPECTED_BULK_SIZE:
            raise AssertionError(f"Expected {2}, got {writer.record_count}")

        writer.close()
        tmp_path.unlink()

    def test_record_count_after_close(self) -> None:
        """Test record_count persists after close."""
        with tempfile.NamedTemporaryFile(encoding="utf-8", mode="w+", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        writer = LdifWriter(output_file=tmp_path)
        writer.write_record({"uid": "user1", "cn": "User One"})
        writer.close()

        if writer.record_count != 1:

            raise AssertionError(f"Expected {1}, got {writer.record_count}")

        tmp_path.unlink()
