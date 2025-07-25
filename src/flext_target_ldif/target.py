"""Main Singer Target implementation for LDIF output."""

# MIGRATED: Singer SDK imports centralized via flext-meltano
from __future__ import annotations

import typing as t
from pathlib import Path

from flext_meltano import th
from flext_meltano.singer import FlextMeltanoTarget as Target

from flext_target_ldif.sinks import LDIFSink


class TargetLDIF(Target):
    """Singer target for writing data to LDIF format."""

    name: str = "target-ldif"

    config_jsonschema: t.ClassVar = th.PropertiesList(
        th.Property(
            "output_path",
            th.StringType,
            description="Directory path for LDIF output files",
            default="./output",
        ),
        th.Property(
            "file_naming_pattern",
            th.StringType,
            description=(
                "Pattern for LDIF file names. Available variables: "
                "{stream_name}, {timestamp}"
            ),
            default="{stream_name}_{timestamp}.ldif",
        ),
        th.Property(
            "ldif_options",
            th.ObjectType(
                th.Property("line_length", th.IntegerType, default=78),
                th.Property("base64_encode", th.BooleanType, default=False),
                th.Property("include_timestamps", th.BooleanType, default=True),
            ),
            description="LDIF format options",
        ),
        th.Property(
            "dn_template",
            th.StringType,
            description="Template for generating Distinguished Names (DN)",
            default="uid={uid},ou=users,dc=example,dc=com",
        ),
        th.Property(
            "attribute_mapping",
            th.ObjectType(),
            description="Mapping of stream fields to LDAP attributes",
            default={},
        ),
    ).to_dict()

    default_sink_class: t.ClassVar = LDIFSink

    def __init__(
        self,
        config: dict[str, t.Any] | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        """Initialize the LDIF target."""
        super().__init__(
            config=config,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )

        # Ensure output directory exists
        output_path = Path(self.config["output_path"])
        output_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    TargetLDIF.cli()
