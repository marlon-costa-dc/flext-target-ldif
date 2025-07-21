"""Tests for configuration utilities."""

import tempfile
from pathlib import Path
from typing import Any

import pytest

from flext_target_ldif.config import (
    ConfigValidationError,
    get_default_attribute_mapping,
    validate_config,
    validate_dn_template,
    validate_output_path,
)


class TestValidateOutputPath:
    """Test output path validation."""

    def test_valid_existing_directory(self) -> None:
        """Test validation of existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_output_path(temp_dir)
            assert Path(result).is_absolute()
            assert Path(result).is_dir()

    def test_create_missing_directory(self) -> None:
        """Test creation of missing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = Path(temp_dir) / "new_subdir"
            result = validate_output_path(str(new_dir))
            assert Path(result).exists()
            assert Path(result).is_dir()

    def test_nested_directory_creation(self) -> None:
        """Test creation of nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "level1" / "level2" / "level3"
            result = validate_output_path(str(nested_dir))
            assert Path(result).exists()
            assert Path(result).is_dir()

    def test_file_as_output_path(self) -> None:
        """Test error when output path is a file."""
        with (
            tempfile.NamedTemporaryFile() as temp_file,
            pytest.raises(ValueError, match="must be a directory"),
        ):
            validate_output_path(temp_file.name)


class TestValidateDnTemplate:
    """Test DN template validation."""

    def test_valid_dn_template(self) -> None:
        """Test validation of valid DN templates."""
        valid_templates = [
            "uid={uid},ou=users,dc=example,dc=com",
            "cn={cn},ou=people,dc=company,dc=org",
            "mail={email},ou=users,dc=test,dc=local",
        ]

        for template in valid_templates:
            result = validate_dn_template(template)
            assert result == template

    def test_empty_dn_template(self) -> None:
        """Test error on empty DN template."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_dn_template("")

    def test_invalid_dn_template_no_equals(self) -> None:
        """Test error on DN template without equals sign."""
        with pytest.raises(ValueError, match="must contain at least one attribute"):
            validate_dn_template("uid{uid},ou_users,dc_example,dc_com")

    def test_minimal_dn_template(self) -> None:
        """Test minimal valid DN template."""
        template = "uid=test"
        result = validate_dn_template(template)
        assert result == template


class TestGetDefaultAttributeMapping:
    """Test default attribute mapping retrieval."""

    def test_default_mapping_structure(self) -> None:
        """Test default attribute mapping contains expected fields."""
        mapping = get_default_attribute_mapping()

        # Check it's a dictionary
        assert isinstance(mapping, dict)

        # Check some expected mappings
        assert mapping["id"] == "uid"
        assert mapping["email"] == "mail"
        assert mapping["first_name"] == "givenName"
        assert mapping["last_name"] == "sn"
        assert mapping["full_name"] == "cn"

    def test_default_mapping_completeness(self) -> None:
        """Test that default mapping covers common fields."""
        mapping = get_default_attribute_mapping()

        expected_fields = [
            "id",
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "display_name",
            "phone",
            "mobile",
            "title",
            "department",
            "organization",
            "description",
            "created_at",
            "updated_at",
        ]

        for field in expected_fields:
            assert field in mapping

    def test_default_mapping_immutable(self) -> None:
        """Test that default mapping returns a copy."""
        mapping1 = get_default_attribute_mapping()
        mapping2 = get_default_attribute_mapping()

        # Modify one mapping
        mapping1["test"] = "test_value"

        # Other mapping should be unchanged
        assert "test" not in mapping2


class TestConfigValidationError:
    """Test ConfigValidationError exception."""

    def test_config_validation_error(self) -> None:
        """Test ConfigValidationError creation and usage."""
        error = ConfigValidationError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

        msg = "Test error"
        with pytest.raises(ConfigValidationError, match="Test error"):
            raise ConfigValidationError(msg)


class TestValidateConfig:
    """Test configuration validation."""

    def test_empty_config(self) -> None:
        """Test validation of empty config."""
        config: dict[str, Any] = {}
        result = validate_config(config)
        assert isinstance(result, dict)

    def test_config_with_output_path(self) -> None:
        """Test config validation with output path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {"output_path": temp_dir}
            result = validate_config(config)
            assert "output_path" in result
            assert Path(result["output_path"]).is_absolute()

    def test_config_with_dn_template(self) -> None:
        """Test config validation with DN template."""
        config = {"dn_template": "uid={uid},ou=users,dc=test,dc=com"}
        result = validate_config(config)
        assert result["dn_template"] == "uid={uid},ou=users,dc=test,dc=com"

    def test_config_with_invalid_dn_template(self) -> None:
        """Test config validation with invalid DN template."""
        config = {"dn_template": ""}
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_config(config)

    def test_config_attribute_mapping_merge(self) -> None:
        """Test that user attribute mapping is merged with defaults."""
        user_mapping = {"custom_field": "customAttr"}
        config = {"attribute_mapping": user_mapping}
        result = validate_config(config)

        # Should contain both default and user mappings
        assert "id" in result["attribute_mapping"]  # Default
        assert "custom_field" in result["attribute_mapping"]  # User
        assert result["attribute_mapping"]["custom_field"] == "customAttr"

    def test_config_user_mapping_overrides_default(self) -> None:
        """Test that user mapping overrides default mapping."""
        user_mapping = {"id": "customUid"}  # Override default mapping
        config = {"attribute_mapping": user_mapping}
        result = validate_config(config)

        assert result["attribute_mapping"]["id"] == "customUid"

    def test_config_ldif_options_validation(self) -> None:
        """Test LDIF options validation."""
        config = {"ldif_options": {"line_length": 50}}
        result = validate_config(config)
        # Should not raise error for valid line length
        assert result is not None

    def test_config_invalid_line_length_type(self) -> None:
        """Test invalid line length type."""
        config = {"ldif_options": {"line_length": "invalid"}}
        with pytest.raises(ConfigValidationError, match="must be an integer"):
            validate_config(config)

    def test_config_invalid_line_length_value(self) -> None:
        """Test invalid line length value."""
        config = {"ldif_options": {"line_length": 5}}
        with pytest.raises(ConfigValidationError, match="must be an integer >= 10"):
            validate_config(config)

    def test_config_no_ldif_options(self) -> None:
        """Test config without LDIF options."""
        config = {"output_path": "./test"}
        result = validate_config(config)
        # Should not fail when ldif_options is not present
        assert "attribute_mapping" in result

    def test_complex_config_validation(self) -> None:
        """Test validation of complex configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {
                "output_path": temp_dir,
                "dn_template": "cn={cn},ou=people,dc=company,dc=com",
                "attribute_mapping": {
                    "employee_id": "employeeNumber",
                    "email": "mail",  # Override default
                },
                "ldif_options": {
                    "line_length": 100,
                    "base64_encode": True,
                },
            }
            result = validate_config(config)

            assert Path(result["output_path"]).is_absolute()
            assert result["dn_template"] == "cn={cn},ou=people,dc=company,dc=com"
            assert result["attribute_mapping"]["employee_id"] == "employeeNumber"
            assert result["attribute_mapping"]["email"] == "mail"
            assert result["attribute_mapping"]["id"] == "uid"  # Default preserved
