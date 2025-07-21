"""LDIF writer implementation for converting records to LDIF format."""

from __future__ import annotations

import base64
import typing as t
from datetime import datetime

if t.TYPE_CHECKING:
    from pathlib import Path


class LDIFWriter:
    """Writer for converting data records to LDIF format."""

    def __init__(
        self,
        output_file: Path,
        ldif_options: dict[str, t.Any] | None = None,
        dn_template: str | None = None,
        attribute_mapping: dict[str, str] | None = None,
        schema: dict[str, t.Any] | None = None,
    ) -> None:
        """Initialize the LDIF writer."""
        self.output_file = output_file
        self.ldif_options = ldif_options or {}
        self.dn_template = dn_template or "uid={uid},ou=users,dc=example,dc=com"
        self.attribute_mapping = attribute_mapping or {}
        self.schema = schema or {}

        # LDIF options
        self.line_length = self.ldif_options.get("line_length", 78)
        self.base64_encode = self.ldif_options.get("base64_encode", False)
        self.include_timestamps = self.ldif_options.get("include_timestamps", True)

        self._file_handle: t.TextIO | None = None
        self._record_count = 0

    def _open_file(self) -> None:
        """Open the output file for writing."""
        if self._file_handle is None:
            self._file_handle = self.output_file.open("w", encoding="utf-8")
            self._write_header()

    def _write_header(self) -> None:
        """Write LDIF header to the file."""
        if not self._file_handle:
            return

        self._file_handle.write("version: 1\n")

        if self.include_timestamps:
            timestamp = datetime.now().isoformat()
            self._file_handle.write(f"# Generated on: {timestamp}\n")
            self._file_handle.write("# FLEXT Target LDIF - Singer Target\n")

        self._file_handle.write("\n")

    def _should_base64_encode(self, value: str) -> bool:
        """Determine if a value should be base64 encoded."""
        if self.base64_encode:
            return True

        # RFC 2849 requires base64 encoding for:
        # - Values starting with space, colon, or less-than
        # - Values containing non-printable characters
        # - Values with trailing spaces

        if not value:
            return False

        if value.startswith((" ", ":", "<")):
            return True

        if value.endswith(" "):
            return True

        # Check for non-printable characters
        return any(ord(char) < 32 or ord(char) > 126 for char in value)

    def _format_value(self, value: t.Any) -> str:
        """Format a value for LDIF output."""
        if value is None:
            return ""

        str_value = str(value)

        if self._should_base64_encode(str_value):
            encoded = base64.b64encode(str_value.encode("utf-8")).decode("ascii")
            return f":: {encoded}"
        return f": {str_value}"

    def _wrap_line(self, line: str) -> str:
        """Wrap long lines according to LDIF format."""
        if len(line) <= self.line_length:
            return line

        result: list[str] = []
        current = line

        while len(current) > self.line_length:
            # Find a good break point
            break_point = self.line_length

            # For continuation lines, start with a space
            if result:
                break_point -= 1

            result.append(current[:break_point])
            current = " " + current[break_point:]

        result.append(current)
        return "\n".join(result)

    def _generate_dn(self, record: dict[str, t.Any]) -> str:
        try:
            return self.dn_template.format(**record)
        except KeyError:
            # If template variable is missing, use a fallback
            uid = record.get("id") or record.get("uid") or str(self._record_count)
            return f"uid={uid},ou=users,dc=example,dc=com"

    def _map_attributes(self, record: dict[str, t.Any]) -> dict[str, t.Any]:
        """Map record fields to LDAP attributes."""
        mapped = {}

        for field, value in record.items():
            # Use explicit mapping if available
            if field in self.attribute_mapping:
                ldap_attr = self.attribute_mapping[field]
            else:
                # Convert field names to LDAP-friendly format
                ldap_attr = field.lower().replace("_", "")

            mapped[ldap_attr] = value

        return mapped

    def write_record(self, record: dict[str, t.Any]) -> None:
        """Write a single record to LDIF format."""
        self._open_file()

        if not self._file_handle:
            msg = "File handle is not available"
            raise RuntimeError(msg)

        # Generate DN
        dn = self._generate_dn(record)

        # Write DN
        dn_line = f"dn{self._format_value(dn)}"
        self._file_handle.write(self._wrap_line(dn_line) + "\n")

        # Map and write attributes
        mapped_attrs = self._map_attributes(record)

        for attr, value in mapped_attrs.items():
            if value is not None:
                attr_line = f"{attr}{self._format_value(value)}"
                self._file_handle.write(self._wrap_line(attr_line) + "\n")

        # Add objectClass if not present
        if "objectclass" not in mapped_attrs:
            self._file_handle.write("objectClass: inetOrgPerson\n")
            self._file_handle.write("objectClass: person\n")

        # Blank line to separate entries
        self._file_handle.write("\n")

        self._record_count += 1

    def close(self) -> None:
        """Close the LDIF file."""
        if self._file_handle:
            if self.include_timestamps:
                self._file_handle.write(
                    f"# Total records written: {self._record_count}\n",
                )

            self._file_handle.close()
            self._file_handle = None
