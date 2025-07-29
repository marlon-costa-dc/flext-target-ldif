"""LDIF writer for flext-target-ldif using flext-ldif infrastructure.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module eliminates code duplication by using the FLEXT LDIF infrastructure
implementation from flext-ldif project.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

from flext_core import FlextResult, get_logger
from flext_ldif import FlextLdifWriter

from flext_target_ldif.exceptions import FlextTargetLdifWriterError

if TYPE_CHECKING:
    import types

logger = get_logger(__name__)

# Use flext-ldif writer instead of reimplementing LDIF writing functionality
LDIFWriter = FlextLdifWriter


class LdifWriter:
    """Writer for converting data records to LDIF format."""

    def __init__(
        self,
        output_file: Path | str | None = None,
        ldif_options: dict[str, Any] | None = None,
        dn_template: str | None = None,
        attribute_mapping: dict[str, str] | None = None,
        schema: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the LDIF writer using flext-ldif infrastructure."""
        self.output_file = Path(output_file) if output_file else Path("output.ldif")
        self.ldif_options = ldif_options or {}
        self.dn_template = dn_template or "uid={uid},ou=users,dc=example,dc=com"
        self.attribute_mapping = attribute_mapping or {}
        self.schema = schema or {}

        # Use flext-ldif writer
        self._writer = FlextLdifWriter()
        self._records: list[dict[str, Any]] = []
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
                # Convert records to LDIF entries format expected by flext-ldif
                ldif_entries = []
                for record in self._records:
                    try:
                        dn = self._generate_dn(record)
                        entry_dict = {"dn": dn}

                        # Apply attribute mapping and add to entry
                        for key, value in record.items():
                            if key != "dn":  # Skip DN as it's already set
                                mapped_key = self.attribute_mapping.get(key, key)
                                entry_dict[mapped_key] = value

                        ldif_entries.append(entry_dict)
                    except (RuntimeError, ValueError, TypeError) as e:
                        logger.warning("Skipping invalid record: %s", e)
                        continue

                # Use flext-ldif writer to write entries
                result = self._writer.write_entries_to_file(
                    self.output_file, ldif_entries,
                )
                if not result.success:
                    return FlextResult.fail(
                        f"Failed to write LDIF file: {result.error}",
                    )

            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to close LDIF file: {e}")

    def write_record(self, record: dict[str, Any]) -> FlextResult[None]:
        """Write a record to the LDIF file buffer."""
        try:
            # Buffer the record for batch writing
            self._records.append(record.copy())
            self._record_count += 1
            return FlextResult.ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to buffer record: {e}")

    def _generate_dn(self, record: dict[str, Any]) -> str:
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
    "LDIFWriter",
    "LdifWriter",
]
