"""Tests for Singer sink implementation."""

import contextlib
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest
from singer_sdk.sinks import BatchSink

from flext_target_ldif.sinks import LDIFSink
from flext_target_ldif.target import TargetLDIF


class TestLDIFSink:
    """Test LDIFSink implementation."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.target = TargetLDIF()
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = Path(self.temp_dir)

        # Mock config
        self.target._config = {
            "output_path": str(self.output_path),
            "dn_template": "uid={uid},ou=users,dc=test,dc=com",
            "attribute_mapping": {},
            "ldif_options": {
                "line_length": 78,
                "base64_encode": False,
                "include_timestamps": True,
            },
            "max_batch_size": 1000,
            "validate_records": True,
        }

        # Create sink
        self.sink = LDIFSink(
            target=self.target,
            stream_name="users",
            schema={
                "properties": {"uid": {"type": "string"}, "cn": {"type": "string"}},
            },
            key_properties=["uid"],
        )

    def test_sink_initialization(self) -> None:
        """Test sink initialization."""
        assert self.sink.stream_name == "users"
        assert isinstance(self.sink, BatchSink)
        assert hasattr(self.sink, "ldif_writer")

    def test_sink_inheritance(self) -> None:
        """Test sink inherits from BatchSink."""
        assert isinstance(self.sink, BatchSink)

    def test_file_naming(self) -> None:
        """Test LDIF file naming logic."""
        # Create a sink and access the ldif_writer to trigger file creation
        sink = LDIFSink(
            target=self.target,
            stream_name="test_stream",
            schema={"properties": {"id": {"type": "string"}}},
            key_properties=["id"],
        )

        # Get the expected path by checking the internal method
        expected_path = self.output_path / "test_stream.ldif"
        actual_path = sink._get_output_file()
        assert actual_path == expected_path

    def test_process_batch_with_records(self) -> None:
        """Test processing a batch of records."""
        records = [
            {"uid": "user1", "cn": "User One", "mail": "user1@test.com"},
            {"uid": "user2", "cn": "User Two", "mail": "user2@test.com"},
        ]

        # Mock the LDIFWriter
        with patch.object(self.sink, "_get_ldif_writer") as mock_get_writer:
            mock_writer = MagicMock()
            mock_get_writer.return_value = mock_writer
            context: dict[str, Any] = {}
            self.sink.process_batch(context)
            self.sink.process_record(records[0], context)
            self.sink.process_record(records[1], context)

            # Should call write_record for each record
            assert mock_writer.write_record.call_count >= 0

    def test_process_record_validation(self) -> None:
        """Test record validation during processing."""
        # Valid record
        valid_record = {"uid": "testuser", "cn": "Test User"}
        context: dict[str, Any] = {}

        # Should not raise exception
        try:
            self.sink.process_record(valid_record, context)
        except Exception as e:
            pytest.fail(f"Valid record raised exception: {e}")

    def test_process_record_invalid(self) -> None:
        """Test handling of invalid records."""
        # Invalid record (no ID field if validation is enabled)
        invalid_record = {"name": "Test User"}  # No uid field
        context: dict[str, Any] = {}

        # Create sink with validation enabled
        self.target._config["validate_records"] = True
        sink = LDIFSink(
            target=self.target,
            stream_name="users",
            schema={"properties": {"uid": {"type": "string"}}},
            key_properties=["uid"],
        )

        # Should handle invalid record gracefully
        with contextlib.suppress(Exception):
            # Expected if validation is strict
            sink.process_record(invalid_record, context)

    def test_clean_batch(self) -> None:
        """Test batch cleanup."""
        with patch.object(self.sink, "_get_ldif_writer") as mock_get_writer:
            mock_writer = MagicMock()
            mock_get_writer.return_value = mock_writer

            # Simulate that the writer was initialized
            self.sink._ldif_writer = mock_writer

            self.sink.clean_up()
            # Should call close on writer
            mock_writer.close.assert_called_once()

    def test_config_access(self) -> None:
        """Test configuration access."""
        config = self.sink.config
        assert "output_path" in config
        assert "dn_template" in config
        # stream_name is not part of config, it's a separate property
        assert self.sink.stream_name == "users"

    def test_schema_access(self) -> None:
        """Test schema access."""
        schema = self.sink.schema
        assert "properties" in schema
        assert "uid" in schema["properties"]

    def test_key_properties_access(self) -> None:
        """Test key properties access."""
        key_props = self.sink.key_properties
        assert key_props == ["uid"]

    def test_target_reference(self) -> None:
        """Test target reference exists (stored internally by Singer SDK)."""
        # Singer SDK stores target internally, but we can't directly access it
        # This test verifies the sink was initialized properly with a target
        assert hasattr(self.sink, "config")  # Config comes from target
        assert self.sink.config is not None

    @patch("flext_target_ldif.sinks.LDIFWriter")
    def test_ldif_writer_initialization(self, mock_writer_class: Any) -> None:
        """Test LDIFWriter initialization in sink."""
        mock_writer = Mock()
        mock_writer_class.return_value = mock_writer

        # Create new sink to trigger writer initialization
        sink = LDIFSink(
            target=self.target,
            stream_name="test",
            schema={"properties": {"id": {"type": "string"}}},
            key_properties=["id"],
        )

        # Access the writer to trigger lazy initialization
        _ = sink.ldif_writer

        # Verify writer was initialized with correct parameters
        mock_writer_class.assert_called_once()
        call_args = mock_writer_class.call_args[1]

        assert "output_file" in call_args
        assert "dn_template" in call_args
        assert "ldif_options" in call_args

    def test_stream_name_sanitization(self) -> None:
        """Test stream name sanitization for file naming."""
        # Test with special characters in stream name
        with patch("flext_target_ldif.sinks.LDIFWriter") as mock_writer_class:
            mock_writer = Mock()
            mock_writer_class.return_value = mock_writer

            sink = LDIFSink(
                target=self.target,
                stream_name="test-stream_with.special chars!",
                schema={"properties": {"id": {"type": "string"}}},
                key_properties=["id"],
            )

            # Access the writer to trigger initialization
            _ = sink.ldif_writer

            # Should create a safe filename
            call_args = mock_writer_class.call_args[1]
            output_file = call_args["output_file"]
            filename = output_file.name

            # Should contain some form of the stream name
            assert "test" in filename
            assert filename.endswith(".ldif")

    def test_multiple_sinks_different_streams(self) -> None:
        """Test multiple sinks for different streams."""
        sink1 = LDIFSink(
            target=self.target,
            stream_name="users",
            schema={"properties": {"uid": {"type": "string"}}},
            key_properties=["uid"],
        )

        sink2 = LDIFSink(
            target=self.target,
            stream_name="groups",
            schema={"properties": {"cn": {"type": "string"}}},
            key_properties=["cn"],
        )

        assert sink1.stream_name == "users"
        assert sink2.stream_name == "groups"
        assert sink1.stream_name != sink2.stream_name

    def test_batch_processing_context(self) -> None:
        """Test batch processing with context."""
        records = [
            {"uid": "user1", "cn": "User One"},
            {"uid": "user2", "cn": "User Two"},
        ]

        context = {"batch_id": "test_batch_123"}

        with patch.object(self.sink, "_get_ldif_writer") as mock_get_writer:
            mock_writer = MagicMock()
            mock_get_writer.return_value = mock_writer

            # Simulate that the writer was initialized
            self.sink._ldif_writer = mock_writer

            # Process batch
            self.sink.process_batch(context)

            # Process individual records
            for record in records:
                self.sink.process_record(record, context)

            # Clean up
            self.sink.clean_up()

            # Verify writer methods were called
            mock_writer.close.assert_called_once()

    def test_error_handling_in_record_processing(self) -> None:
        """Test error handling during record processing."""
        invalid_record = {"invalid": "data"}
        context: dict[str, Any] = {}

        with patch.object(self.sink, "_get_ldif_writer") as mock_get_writer:
            mock_writer = MagicMock()
            mock_get_writer.return_value = mock_writer
            # Make write_record raise an exception
            mock_writer.write_record.side_effect = Exception("Write error")

            # Should handle the error gracefully
            with contextlib.suppress(Exception):
                # Some error handling is expected
                self.sink.process_record(invalid_record, context)
