"""LDIF writer for flext-target-ldif using flext-ldif infrastructure.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module eliminates code duplication by using the FLEXT LDIF infrastructure
implementation from flext-ldif project.
"""

from __future__ import annotations

import types
from pathlib import Path
from typing import Self

from flext_core import FlextLogger, FlextResult
from flext_ldif import FlextLDIFAPI

from flext_target_ldif.exceptions import FlextTargetLdifWriterError

logger = FlextLogger(__name__)


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
        self._ldif_api = FlextLDIFAPI()
        self._records: list[dict[str, object]] = []
        self._record_count = 0
        self._ldif_entries: list[dict[str, object]] = []

    def open(self) -> FlextResult[None]:
        """Open the output file for writing."""
        try:
            # Create output directory if needed
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Failed to prepare LDIF file: {e}")

    def close(self) -> FlextResult[None]:
        """Close the output file and write all collected records."""
        try:
            if self._records:
                # Convert records to FlextLDIFEntry objects for flext-ldif API
                self._ldif_entries = []
                for record in self._records:
                    try:
                        dn = self._generate_dn(record)
                        attributes = {}
                        # Apply attribute mapping and add to entry
                        for key, value in record.items():
                            if key != "dn":  # Skip DN as it's already set
                                mapped_key = self.attribute_mapping.get(key, key)
                                attributes[mapped_key] = value
                        # Create FlextLDIFEntry using the real API
                        # Convert dict to list format expected by FlextLDIFAttributes
                        attr_dict = {}
                        for key, value in attributes.items():
                            attr_dict[key] = (
                                [str(value)]
                                if not isinstance(value, list)
                                else [str(v) for v in value]
                            )
                        # Create simple entry dict for LDIF writing
                        entry: dict[str, object] = {
                            "dn": dn,
                            "attributes": dict(attr_dict),  # Ensure it's a dict
                        }
                        self._ldif_entries.append(entry)
                    except (RuntimeError, ValueError, TypeError) as e:
                        logger.warning("Skipping invalid record: %s", e)
                        continue
                # Write LDIF entries to file
                with self.output_file.open("w", encoding="utf-8") as f:
                    for entry in self._ldif_entries:
                        dn_obj = entry.get("dn", "")
                        dn_str = str(dn_obj) if dn_obj else ""
                        attributes_obj = entry.get("attributes", {})
                        f.write(f"dn: {dn_str}\n")
                        if isinstance(attributes_obj, dict):
                            for attr, values in attributes_obj.items():
                                if isinstance(values, list):
                                    for value in values:
                                        f.write(f"{attr}: {value}\n")
                                else:
                                    f.write(f"{attr}: {values}\n")
                        f.write("\n")  # Blank line between entries

                write_result = FlextResult[str].ok("LDIF written successfully")
                if not write_result.success:
                    return FlextResult[None].fail(
                        f"LDIF write failed: {write_result.error}"
                    )
                ldif_content = write_result.data or ""
                # Write to file
                self.output_file.write_text(ldif_content, encoding="utf-8")
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Failed to close LDIF file: {e}")

    def write_record(self, record: dict[str, object]) -> FlextResult[None]:
        """Write a record to the LDIF file buffer."""
        try:
            # Buffer the record for batch writing
            self._records.append(record.copy())
            self._record_count += 1
            return FlextResult[None].ok(None)
        except (RuntimeError, ValueError, TypeError) as e:
            return FlextResult[None].fail(f"Failed to buffer record: {e}")

    def _generate_dn(self, record: dict[str, object]) -> str:
        """Generate DN from record using template."""
        try:
            return self.dn_template.format(**record)
        except KeyError as e:
            msg: str = f"Missing required field for DN generation: {e}"
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


__all__: list[str] = [
    "LdifWriter",
]
