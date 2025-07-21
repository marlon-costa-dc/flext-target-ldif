"""Tests for FLEXT Target LDIF main target implementation."""

import tempfile
from pathlib import Path

import pytest

from flext_target_ldif.target import TargetLDIF


class TestTargetLDIF:
    """Test cases for TargetLDIF class."""

    def test_target_initialization(self) -> None:
        """Test basic target initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {
                "output_path": temp_dir,
            }
            target = TargetLDIF(config=config)

            assert target.name == "target-ldif"
            assert target.config["output_path"] == temp_dir

            # Check that output directory exists
            assert Path(temp_dir).is_dir()

    def test_target_config_schema(self) -> None:
        """Test target configuration schema."""
        schema = TargetLDIF.config_jsonschema

        # Check required properties exist
        properties = schema["properties"]
        assert "output_path" in properties
        assert "file_naming_pattern" in properties
        assert "dn_template" in properties
        assert "ldif_options" in properties
        assert "attribute_mapping" in properties

    def test_target_default_config(self) -> None:
        """Test target with default configuration."""
        target = TargetLDIF()

        # Check defaults
        assert target.config["output_path"] == "./output"
        assert target.config["file_naming_pattern"] == "{stream_name}_{timestamp}.ldif"
        assert target.config["dn_template"] == "uid={uid},ou=users,dc=example,dc=com"

    def test_target_custom_config(self) -> None:
        """Test target with custom configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {
                "output_path": temp_dir,
                "file_naming_pattern": "custom_{stream_name}.ldif",
                "dn_template": "cn={cn},ou=people,dc=test,dc=com",
                "ldif_options": {
                    "line_length": 100,
                    "base64_encode": True,
                    "include_timestamps": False,
                },
                "attribute_mapping": {
                    "user_id": "uid",
                    "name": "cn",
                },
            }

            target = TargetLDIF(config=config)

            assert target.config["output_path"] == temp_dir
            assert target.config["file_naming_pattern"] == "custom_{stream_name}.ldif"
            assert target.config["dn_template"] == "cn={cn},ou=people,dc=test,dc=com"
            assert target.config["ldif_options"]["line_length"] == 100
            assert target.config["attribute_mapping"]["user_id"] == "uid"

    def test_output_directory_creation(self) -> None:
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "new_directory"

            config = {
                "output_path": str(output_path),
            }

            # Directory shouldn't exist yet
            assert not output_path.exists()

            # Initialize target
            TargetLDIF(config=config)

            # Directory should now exist
            assert output_path.is_dir()

    @pytest.mark.integration
    def test_target_cli_entry_point(self) -> None:
        """Test that target can be instantiated via CLI."""
        # This would be a more complex integration test
        # For now, just test that the CLI method exists
        assert hasattr(TargetLDIF, "cli")
        assert callable(TargetLDIF.cli)
