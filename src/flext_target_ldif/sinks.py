"""Singer Sink implementation for LDIF output."""

from __future__ import annotations

from pathlib import Path

# MIGRATED: BatchSink now consolidated in flext-meltano
from flext_meltano import BatchSink, Target

from flext_target_ldif.writer import LdifWriter


class LDIFSink(BatchSink):
    """Singer sink for writing records to LDIF format."""

    def __init__(
        self,
        target: Target,
        stream_name: str,
        schema: dict[str, object],
        key_properties: list[str] | None = None,
    ) -> None:
        """Initialize the LDIF sink."""
        super().__init__(target, stream_name, schema, key_properties)

        self._ldif_writer: LdifWriter | None = None
        self._output_file: Path | None = None

    def _get_output_file(self) -> Path:
        """Get the output file path for this stream."""
        if self._output_file is None:
            output_path = Path(self.config.get("output_path", "./output"))

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
            self._ldif_writer = LdifWriter(
                output_file=output_file,
                ldif_options=self.config.get("ldif_options", {}),
                dn_template=self.config.get("dn_template"),
                attribute_mapping=self.config.get("attribute_mapping", {}),
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
                self.logger.error(f"Failed to close LDIF writer: {result.error}")
            elif hasattr(self, "logger"):
                self.logger.info(f"LDIF file written: {self._output_file}")

    @property
    def ldif_writer(self) -> LdifWriter:
        """Get the LDIF writer (for testing)."""
        return self._get_ldif_writer()
