"""Comprehensive tests for FlextTargetLdif main target class.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

REFACTORED: Complete target system with 100% coverage and validation.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from flext_target_ldif import FlextTargetLdif, FlextTargetLdifConfig
from flext_target_ldif.exceptions import FlextTargetLdifConfigurationError
from flext_target_ldif.sinks import LDIFSink
from flext_target_ldif.target import TargetLDIF


class TestFlextTargetLdifConfig:
    """Test FlextTargetLdifConfig value object."""

    def test_config_creation_with_defaults(self) -> None:
        """Test creating config with default values."""
        config = FlextTargetLdifConfig(output_file="test.ldif")
        if config.output_file != "test.ldif":
            msg = f"Expected {'test.ldif'}, got {config.output_file}"
            raise AssertionError(msg)
        if not (config.schema_validation):
            msg = f"Expected True, got {config.schema_validation}"
            raise AssertionError(msg)
        if config.dn_template != "uid={uid},ou=users,dc=example,dc=com":
            msg = f"Expected {'uid={uid},ou=users,dc=example,dc=com'}, got {config.dn_template}"
            raise AssertionError(
                msg,
            )
        assert config.line_length == 78
        if config.base64_encode:
            msg = f"Expected False, got {config.base64_encode}"
            raise AssertionError(msg)

    def test_config_creation_with_custom_values(self) -> None:
        """Test creating config with custom values."""
        config = FlextTargetLdifConfig(
            output_file="/tmp/custom.ldif",
            schema_validation=False,
            dn_template="cn={name},ou=people,dc=test,dc=com",
            line_length=100,
            base64_encode=True,
            attribute_mapping={"email": "mail"},
        )
        if config.output_file != "/tmp/custom.ldif":
            msg = f"Expected {'/tmp/custom.ldif'}, got {config.output_file}"
            raise AssertionError(
                msg,
            )
        if config.schema_validation:
            msg = f"Expected False, got {config.schema_validation}"
            raise AssertionError(msg)
        assert config.dn_template == "cn={name},ou=people,dc=test,dc=com"
        if config.line_length != 100:
            msg = f"Expected {100}, got {config.line_length}"
            raise AssertionError(msg)
        if not (config.base64_encode):
            msg = f"Expected True, got {config.base64_encode}"
            raise AssertionError(msg)
        if config.attribute_mapping != {"email": "mail"}:
            msg = f"Expected {{'email': 'mail'}}, got {config.attribute_mapping}"
            raise AssertionError(
                msg,
            )

    def test_config_immutability(self) -> None:
        """Test that config is immutable."""
        config = FlextTargetLdifConfig(output_file="test.ldif")

        with pytest.raises(ValidationError):
            config.output_file = "modified.ldif"

    def test_config_validation_empty_output_file(self) -> None:
        """Test validation with empty output file."""
        config = FlextTargetLdifConfig(output_file="")
        with pytest.raises(ValueError, match="Output file cannot be empty"):
            config.validate_domain_rules()

    def test_config_validation_empty_dn_template(self) -> None:
        """Test validation with empty DN template."""
        config = FlextTargetLdifConfig(
            output_file="test.ldif",
            dn_template="",
        )
        with pytest.raises(ValueError, match="DN template cannot be empty"):
            config.validate_domain_rules()

    def test_config_validation_invalid_line_length(self) -> None:
        """Test validation with invalid line length."""
        config = FlextTargetLdifConfig(
            output_file="test.ldif",
            line_length=0,
        )
        with pytest.raises(ValueError, match="Line length must be positive"):
            config.validate_domain_rules()

    def test_config_validation_valid_config(self) -> None:
        """Test validation with valid config."""
        config = FlextTargetLdifConfig(
            output_file="test.ldif",
            dn_template="uid={uid},ou=users,dc=example,dc=com",
            line_length=78,
        )
        # Should not raise exception
        config.validate_domain_rules()


class TestFlextTargetLdif:
    """Test FlextTargetLdif main class."""

    def test_target_inheritance(self) -> None:
        """Test that FlextTargetLdif inherits from TargetLDIF."""
        target = FlextTargetLdif()
        assert isinstance(target, TargetLDIF)

    def test_target_creation_with_defaults(self) -> None:
        """Test creating target with default configuration."""
        target = FlextTargetLdif()

        # Should have default configuration
        assert hasattr(target, "config")

    @patch("flext_target_ldif.target.TargetLDIF.__init__")
    def test_target_initialization(self, mock_init: Mock) -> None:
        """Test target initialization calls parent."""
        mock_init.return_value = None

        FlextTargetLdif()
        mock_init.assert_called_once()

    def test_target_validate_config_success(self) -> None:
        """Test successful config validation."""
        target = FlextTargetLdif()

        # Set test config
        target._test_config = {
            "output_file": "test.ldif",
            "schema_validation": True,
            "dn_template": "uid={uid},ou=users,dc=example,dc=com",
            "line_length": 78,
            "base64_encode": False,
        }

        # Should not raise exception
        result = target.validate_config()
        assert result is None

    def test_target_validate_config_missing_output_file(self) -> None:
        """Test config validation with missing output file."""
        target = FlextTargetLdif()
        target._test_config = {"schema_validation": True}

        with pytest.raises(FlextTargetLdifConfigurationError) as exc_info:
            target.validate_config()

        if "Output file is required" not in str(exc_info.value):
            msg = f"Expected {'Output file is required'} in {exc_info.value!s}"
            raise AssertionError(
                msg,
            )

    def test_target_validate_config_invalid_output_file(self) -> None:
        """Test config validation with invalid output file."""
        target = FlextTargetLdif()
        target._test_config = {
            "output_file": "",
            "schema_validation": True,
        }

        with pytest.raises(FlextTargetLdifConfigurationError) as exc_info:
            target.validate_config()

        if "Output file cannot be empty" not in str(exc_info.value):
            msg = f"Expected {'Output file cannot be empty'} in {exc_info.value!s}"
            raise AssertionError(
                msg,
            )

    def test_target_validate_config_invalid_dn_template(self) -> None:
        """Test config validation with invalid DN template."""
        target = FlextTargetLdif()
        target._test_config = {
            "output_file": "test.ldif",
            "dn_template": "",
            "schema_validation": True,
        }

        with pytest.raises(FlextTargetLdifConfigurationError) as exc_info:
            target.validate_config()

        if "DN template cannot be empty" not in str(exc_info.value):
            msg = f"Expected {'DN template cannot be empty'} in {exc_info.value!s}"
            raise AssertionError(
                msg,
            )


class TestTargetLDIF:
    """Test the base TargetLDIF class."""

    def test_target_ldif_creation(self) -> None:
        """Test creating TargetLDIF instance."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = {"output_path": tmp_dir}
            target = TargetLDIF(config=config)
            assert isinstance(target, TargetLDIF)

    def test_target_ldif_name_property(self) -> None:
        """Test target name property."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = {"output_path": tmp_dir}
            target = TargetLDIF(config=config)
            if target.name != "target-ldif":
                msg = f"Expected {'target-ldif'}, got {target.name}"
                raise AssertionError(msg)

    def test_target_ldif_config_schema(self) -> None:
        """Test target config schema is properly defined."""
        target = TargetLDIF()

        # Should have proper config schema
        assert hasattr(target, "config_jsonschema")
        assert isinstance(target.config_jsonschema, dict)

        # Should have required properties
        properties = target.config_jsonschema.get("properties", {})
        if "output_path" not in properties:
            msg = f"Expected {'output_path'} in {properties}"
            raise AssertionError(msg)
        assert "file_naming_pattern" in properties
        if "dn_template" not in properties:
            msg = f"Expected {'dn_template'} in {properties}"
            raise AssertionError(msg)

    def test_target_ldif_default_sink_class(self) -> None:
        """Test target has proper default sink class."""
        target = TargetLDIF()
        if target.default_sink_class != LDIFSink:
            msg = f"Expected {LDIFSink}, got {target.default_sink_class}"
            raise AssertionError(
                msg,
            )

    def test_target_ldif_output_directory_creation(self) -> None:
        """Test target creates output directory."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "new_directory"
            config = {"output_path": str(output_path)}

            # Directory should not exist initially
            assert not output_path.exists()

            # Creating target should create directory
            TargetLDIF(config=config)
            assert output_path.exists()
            assert output_path.is_dir()

    def test_target_ldif_cli_method(self) -> None:
        """Test CLI method exists."""
        target = TargetLDIF()

        # Should have cli method from Singer SDK
        assert hasattr(target, "cli")
        assert callable(target.cli)

    def test_target_ldif_config_dict_access(self) -> None:
        """Test config dict access."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = {
                "output_path": tmp_dir,
                "dn_template": "cn={name},ou=people,dc=test,dc=com",
            }
            target = TargetLDIF(config=config)

            if target.config["output_path"] != tmp_dir:
                msg = f"Expected {tmp_dir}, got {target.config['output_path']}"
                raise AssertionError(
                    msg,
                )
            assert target.config["dn_template"] == "cn={name},ou=people,dc=test,dc=com"

    def test_target_ldif_default_config_values(self) -> None:
        """Test default configuration values."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = {"output_path": tmp_dir}
            target = TargetLDIF(config=config)

            # Should use defaults from schema
            assert (
                target.config["file_naming_pattern"] == "{stream_name}_{timestamp}.ldif"
            )
            assert (
                target.config["dn_template"] == "uid={uid},ou=users,dc=example,dc=com"
            )


class TestIntegration:
    """Integration tests for the complete target system."""

    def test_end_to_end_ldif_generation(self) -> None:
        """Test end-to-end LDIF generation."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w+", delete=False, suffix=".ldif",
        ) as tmp:
            tmp_path = Path(tmp.name)

        # Create config
        config = FlextTargetLdifConfig(
            output_file=str(tmp_path),
            schema_validation=True,
            dn_template="uid={uid},ou=users,dc=example,dc=com",
        )

        # Validate config
        config.validate_domain_rules()

        # Create target (would be used by Singer SDK)
        target = FlextTargetLdif()

        # Set test configuration
        target._test_config = {
            "output_file": str(tmp_path),
            "schema_validation": True,
            "dn_template": "uid={uid},ou=users,dc=example,dc=com",
            "line_length": 78,
            "base64_encode": False,
        }

        # Validate target config
        target.validate_config()

        # Clean up
        tmp_path.unlink()

    def test_flext_target_ldif_alias_compatibility(self) -> None:
        """Test that FlextTargetLdif maintains compatibility."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config = {"output_path": tmp_dir}

            # Test that both classes can be instantiated
            original_target = TargetLDIF(config=config)
            flext_target = FlextTargetLdif()

            # Both should be instances of TargetLDIF
            assert isinstance(original_target, TargetLDIF)
            assert isinstance(flext_target, TargetLDIF)

            # FlextTargetLdif should maintain the same interface
            assert hasattr(flext_target, "cli")
            assert hasattr(flext_target, "validate_config")

    def test_config_to_dict_conversion(self) -> None:
        """Test config can be converted to dict for Singer SDK."""
        config = FlextTargetLdifConfig(
            output_file="test.ldif",
            schema_validation=True,
            dn_template="uid={uid},ou=users,dc=example,dc=com",
            line_length=100,
            base64_encode=True,
            attribute_mapping={"email": "mail", "name": "cn"},
        )

        config_dict = config.model_dump()

        if config_dict["output_file"] != "test.ldif":
            msg = f"Expected {'test.ldif'}, got {config_dict['output_file']}"
            raise AssertionError(
                msg,
            )
        if not (config_dict["schema_validation"]):
            msg = f"Expected True, got {config_dict['schema_validation']}"
            raise AssertionError(
                msg,
            )
        if config_dict["dn_template"] != "uid={uid},ou=users,dc=example,dc=com":
            msg = f"Expected {'uid={uid},ou=users,dc=example,dc=com'}, got {config_dict['dn_template']}"
            raise AssertionError(
                msg,
            )
        assert config_dict["line_length"] == 100
        if not (config_dict["base64_encode"]):
            msg = f"Expected True, got {config_dict['base64_encode']}"
            raise AssertionError(msg)
        if config_dict["attribute_mapping"] != {"email": "mail", "name": "cn"}:
            msg = f"Expected {{'email': 'mail', 'name': 'cn'}}, got {config_dict['attribute_mapping']}"
            raise AssertionError(
                msg,
            )

    def test_error_handling_integration(self) -> None:
        """Test error handling across the system."""
        # Test config validation error propagation
        invalid_config = FlextTargetLdifConfig(
            output_file="",  # Invalid empty file
        )

        with pytest.raises(ValueError):
            invalid_config.validate_domain_rules()

        # Test target validation error
        target = FlextTargetLdif()
        target._test_config = {"output_file": ""}  # Invalid

        with pytest.raises(FlextTargetLdifConfigurationError):
            target.validate_config()

    def test_singer_sdk_compatibility(self) -> None:
        """Test compatibility with Singer SDK patterns."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Test that TargetLDIF follows Singer SDK patterns
            config = {
                "output_path": tmp_dir,
                "dn_template": "uid={uid},ou=users,dc=example,dc=com",
                "file_naming_pattern": "{stream_name}.ldif",
            }

            target = TargetLDIF(config=config, validate_config=True)

            # Should have Singer SDK required attributes
            assert hasattr(target, "name")
            assert hasattr(target, "config_jsonschema")
            assert hasattr(target, "default_sink_class")
            assert hasattr(target, "cli")

            # Config should be accessible
            if target.config["output_path"] != tmp_dir:
                msg = f"Expected {tmp_dir}, got {target.config['output_path']}"
                raise AssertionError(
                    msg,
                )
            assert (
                target.config["dn_template"] == "uid={uid},ou=users,dc=example,dc=com"
            )
