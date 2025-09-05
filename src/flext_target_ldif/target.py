"""Main Singer Target implementation for LDIF output."""

# MIGRATED: Singer SDK imports centralized via flext-meltano
from __future__ import annotations

from pathlib import Path

from flext_target_ldif.sinks import LDIFSink


class TargetLDIF:
    """Singer target for writing data to LDIF format."""

    name: str = "target-ldif"

    def __init__(
        self,
        config: dict[str, object] | None = None,
    ) -> None:
        """Initialize the LDIF target."""
        self.config = config or {}
        self.sinks: dict[str, LDIFSink] = {}

        # Ensure output directory exists
        output_path_str = self.config.get("output_path", "./output")
        if not isinstance(output_path_str, str):
            output_path_str = "./output"
        output_path = Path(output_path_str)
        output_path.mkdir(parents=True, exist_ok=True)

    def get_sink(self, stream_name: str, schema: dict[str, object]) -> LDIFSink:
        """Get or create a sink for the given stream."""
        if stream_name not in self.sinks:
            self.sinks[stream_name] = LDIFSink(
                target_config=self.config,
                stream_name=stream_name,
                schema=schema,
            )
        return self.sinks[stream_name]


if __name__ == "__main__":
    # Use flext-target-ldif CLI entry point instead
    pass
