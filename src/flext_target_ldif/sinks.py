"""Singer Sink implementation for LDIF output."""

from __future__ import annotations

from pathlib import Path

# Use available flext-meltano abstractions
from flext_target_ldif.writer import LdifWriter


class LDIFSink:
    """Singer sink for writing records to LDIF format."""

    def __init__(
        self,
        target_config: dict[str, object],
        stream_name: str,
        schema: dict[str, object],
        key_properties: list[str] | None = None,
    ) -> None:
        """Initialize the LDIF sink."""
        self.config = target_config
        self.stream_name = stream_name
        self.schema = schema
        self.key_properties = key_properties or []

        self._ldif_writer: LdifWriter | None = None
        self._output_file: Path | None = None

    def _get_output_file(self) -> Path:
        """Get the output file path for this stream."""
        if self._output_file is None:
            output_path_str = self.config.get("output_path", "./output")
            if not isinstance(output_path_str, str):
                output_path_str = "./output"
            output_path = Path(output_path_str)

            # Create safe filename from stream name
            safe_name = "".join(
                c for c in self.stream_name if c.isalnum() or c in "-_"
            ).strip()
            if not safe_name:
                safe_name = "stream"

            filename = f"{safe_name}.ldif"
            self._output_file = output_path / filename

        return self._output_file

    def _get_ldif_writer(self) -> LdifWriter:
        """Get or create the LDIF writer for this sink."""
        if self._ldif_writer is None:
            output_file = self._get_output_file()

            # Type-safe config extraction
            ldif_options = self.config.get("ldif_options", {})
            if not isinstance(ldif_options, dict):
                ldif_options = {}

            dn_template = self.config.get("dn_template")
            if dn_template is not None and not isinstance(dn_template, str):
                dn_template = None

            attribute_mapping = self.config.get("attribute_mapping", {})
            if not isinstance(attribute_mapping, dict):
                attribute_mapping = {}

            self._ldif_writer = LdifWriter(
                output_file=output_file,
                ldif_options=ldif_options,
                dn_template=dn_template,
                attribute_mapping=attribute_mapping,
                schema=self.schema,
            )

        return self._ldif_writer

    def process_batch(self, _context: dict[str, object]) -> None:
        """Process a batch of records."""
        # BatchSink handles the batching, we just need to ensure writer is ready
        self._get_ldif_writer()

    def process_record(
        self,
        record: dict[str, object],
        _context: dict[str, object],
    ) -> None:
        """Process a single record and write to LDIF."""
        ldif_writer = self._get_ldif_writer()
        result = ldif_writer.write_record(record)
        if not result.success:
            msg: str = f"Failed to write LDIF record: {result.error}"
            raise RuntimeError(msg)

    def clean_up(self) -> None:
        """Clean up resources when sink is finished."""
        if self._ldif_writer:
            result = self._ldif_writer.close()
            if not result.success and hasattr(self, "logger"):
                self.logger.error("Failed to close LDIF writer: %s", result.error)
            elif hasattr(self, "logger"):
                self.logger.info("LDIF file written: %s", self._output_file)

    @property
    def ldif_writer(self) -> LdifWriter:
        """Get the LDIF writer (for testing)."""
        return self._get_ldif_writer()
