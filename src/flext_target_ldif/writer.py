"""LDIF writer for flext-target-ldif using flext-ldif infrastructure.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module eliminates code duplication by using the FLEXT LDIF infrastructure
implementation from flext-ldif project.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Self

from flext_core import FlextResult, get_logger
from flext_ldif import (
    FlextLdifAttributes,
    FlextLdifDistinguishedName,
    FlextLdifEntry,
    flext_ldif_write,
)

from flext_target_ldif.exceptions import FlextTargetLdifWriterError

if TYPE_CHECKING:
    import types

logger = get_logger(__name__)


class LdifWriter:
    """Writer for converting data records to LDIF format."""

    def __init__(
        self,
        output_file: Path | str | None = None,
        ldif_options: dict[str, object] | None = None,
        dn_template: str | None = None,
        attribute_mapping: dict[str, str] | None = None,
        schema: dict[str, object] | None = None,
    ) -> None:
        """Initialize the LDIF writer using flext-ldif infrastructure."""
        self.output_file = Path(output_file) if output_file else Path("output.ldif")
        self.ldif_options = ldif_options or {}
        self.dn_template = dn_template or "uid={uid},ou=users,dc=example,dc=com"
        self.attribute_mapping = attribute_mapping or {}
        self.schema = schema or {}

        # Use flext-ldif API for writing
        self._records: list[dict[str, object]] = []
        self._record_count = 0

    def open(self) -> FlextResult[None]:
        """Open the output file for writing."""
        try:
            # Create output directory if needed
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to prepare LDIF file: {e}")

    def close(self) -> FlextResult[None]:
        """Close the output file and write all collected records."""
        try:
            if self._records:
                # Convert records to FlextLdifEntry objects for flext-ldif API
                ldif_entries = []
                for record in self._records:
                    try:
                        dn = self._generate_dn(record)
                        attributes = {}

                        # Apply attribute mapping and add to entry
                        for key, value in record.items():
                            if key != "dn":  # Skip DN as it's already set
                                mapped_key = self.attribute_mapping.get(key, key)
                                attributes[mapped_key] = value

                        # Create FlextLdifEntry using the real API
                        # Convert dict to list format expected by FlextLdifAttributes
                        attr_dict = {}
                        for key, value in attributes.items():
                            attr_dict[key] = (
                                [str(value)]
                                if not isinstance(value, list)
                                else [str(v) for v in value]
                            )

                        entry = FlextLdifEntry(
                            dn=FlextLdifDistinguishedName(value=dn),
                            attributes=FlextLdifAttributes(attributes=attr_dict),
                        )
                        ldif_entries.append(entry)
                    except (RuntimeError, ValueError, TypeError) as e:
                        logger.warning("Skipping invalid record: %s", e)
                        continue

                # Use real flext-ldif API to write entries
                ldif_content = flext_ldif_write(ldif_entries, str(self.output_file))

                # Write to file
                self.output_file.write_text(ldif_content, encoding="utf-8")

            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to close LDIF file: {e}")

    def write_record(self, record: dict[str, object]) -> FlextResult[None]:
        """Write a record to the LDIF file buffer."""
        try:
            # Buffer the record for batch writing
            self._records.append(record.copy())
            self._record_count += 1
            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to buffer record: {e}")

    def _generate_dn(self, record: dict[str, object]) -> str:
        """Generate DN from record using template."""
        try:
            return self.dn_template.format(**record)
        except KeyError as e:
            msg = f"Missing required field for DN generation: {e}"
            raise FlextTargetLdifWriterError(msg) from e

    @property
    def record_count(self) -> int:
        """Get the number of records written."""
        return self._record_count

    def __enter__(self) -> Self:
        """Context manager entry."""
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """Context manager exit."""
        self.close()


__all__ = [
    "LdifWriter",
]
