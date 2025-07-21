"""Tests for LDIF writer functionality."""

import tempfile
from pathlib import Path

from flext_target_ldif.ldif_writer import LDIFWriter


class TestLDIFWriter:
    """Test cases for LDIFWriter class."""

    def test_ldif_writer_initialization(self) -> None:
        """Test LDIF writer initialization."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)

            writer = LDIFWriter(output_file=temp_path)

            assert writer.output_file == temp_path
            assert writer.line_length == 78
            assert writer.base64_encode is False
            assert writer.include_timestamps is True

    def test_ldif_writer_custom_options(self) -> None:
        """Test LDIF writer with custom options."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)

            ldif_options = {
                "line_length": 100,
                "base64_encode": True,
                "include_timestamps": False,
            }

            writer = LDIFWriter(
                output_file=temp_path,
                ldif_options=ldif_options,
            )

            assert writer.line_length == 100
            assert writer.base64_encode is True
            assert writer.include_timestamps is False

    def test_base64_encoding_detection(self) -> None:
        """Test base64 encoding detection logic."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)
            writer = LDIFWriter(output_file=temp_path)

            # Values that should be base64 encoded
            assert writer._should_base64_encode(" starts with space")
            assert writer._should_base64_encode(":starts with colon")
            assert writer._should_base64_encode("<starts with less than")
            assert writer._should_base64_encode("ends with space ")
            assert writer._should_base64_encode("has\nnewline")
            assert writer._should_base64_encode("has\ttab")

            # Values that should NOT be base64 encoded
            assert not writer._should_base64_encode("normal text")
            assert not writer._should_base64_encode("email@example.com")
            assert not writer._should_base64_encode("123456")

    def test_value_formatting(self) -> None:
        """Test value formatting for LDIF output."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)
            writer = LDIFWriter(output_file=temp_path)

            # Normal values
            assert writer._format_value("test") == ": test"
            assert writer._format_value(123) == ": 123"
            assert writer._format_value(None) == ""

            # Values requiring base64
            writer.base64_encode = True
            formatted = writer._format_value("test")
            assert formatted.startswith(":: ")
            assert len(formatted) > 3  # Should contain base64 encoded content

    def test_dn_generation(self) -> None:
        """Test DN generation from record data."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)

            writer = LDIFWriter(
                output_file=temp_path,
                dn_template="uid={uid},ou=users,dc=example,dc=com",
            )

            record = {"uid": "testuser", "name": "Test User"}
            dn = writer._generate_dn(record)

            assert dn == "uid=testuser,ou=users,dc=example,dc=com"

    def test_dn_generation_fallback(self) -> None:
        """Test DN generation fallback when template variables are missing."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)

            writer = LDIFWriter(
                output_file=temp_path,
                dn_template="uid={missing_field},ou=users,dc=example,dc=com",
            )

            record = {"name": "Test User"}
            dn = writer._generate_dn(record)

            # Should fall back to default pattern
            assert "uid=" in dn
            assert "ou=users,dc=example,dc=com" in dn

    def test_attribute_mapping(self) -> None:
        """Test attribute mapping functionality."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)

            attribute_mapping = {
                "user_id": "uid",
                "full_name": "cn",
                "email": "mail",
            }

            writer = LDIFWriter(
                output_file=temp_path,
                attribute_mapping=attribute_mapping,
            )

            record = {
                "user_id": "testuser",
                "full_name": "Test User",
                "email": "test@example.com",
                "other_field": "value",
            }

            mapped = writer._map_attributes(record)

            assert mapped["uid"] == "testuser"
            assert mapped["cn"] == "Test User"
            assert mapped["mail"] == "test@example.com"
            assert mapped["otherfield"] == "value"  # Default mapping

    def test_write_single_record(self) -> None:
        """Test writing a single record to LDIF."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w+", delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

            writer = LDIFWriter(
                output_file=temp_path,
                dn_template="uid={uid},ou=users,dc=example,dc=com",
            )

            record = {
                "uid": "testuser",
                "cn": "Test User",
                "mail": "test@example.com",
            }

            writer.write_record(record)
            writer.close()

            # Read the file and verify content
            content = temp_path.read_text(encoding="utf-8")

            assert "version: 1" in content
            assert "dn: uid=testuser,ou=users,dc=example,dc=com" in content
            assert "uid: testuser" in content
            assert "cn: Test User" in content
            assert "mail: test@example.com" in content
            assert "objectClass: inetOrgPerson" in content

    def test_line_wrapping(self) -> None:
        """Test LDIF line wrapping functionality."""
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = Path(temp_file.name)

            writer = LDIFWriter(
                output_file=temp_path,
                ldif_options={"line_length": 20},  # Very short for testing
            )

            long_line = "this_is_a_very_long_line_that_should_be_wrapped"
            wrapped = writer._wrap_line(f"attribute: {long_line}")

            lines = wrapped.split("\n")
            assert len(lines) > 1  # Should be wrapped into multiple lines

            # Continuation lines should start with space
            for line in lines[1:]:
                assert line.startswith(" ")

    def test_multiple_records(self) -> None:
        """Test writing multiple records."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w+", delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

            writer = LDIFWriter(output_file=temp_path)

            records = [
                {"uid": "user1", "cn": "User One"},
                {"uid": "user2", "cn": "User Two"},
                {"uid": "user3", "cn": "User Three"},
            ]

            for record in records:
                writer.write_record(record)

            writer.close()

            content = temp_path.read_text(encoding="utf-8")

            # Should contain all three users
            assert "uid: user1" in content
            assert "uid: user2" in content
            assert "uid: user3" in content

            # Should contain record count comment
            assert "Total records written: 3" in content
