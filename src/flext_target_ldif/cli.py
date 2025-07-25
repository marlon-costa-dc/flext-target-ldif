"""CLI entry point for FlextTargetLdif."""

from __future__ import annotations

from flext_target_ldif.target import TargetLDIF


def main() -> None:
    """Main CLI entry point."""
    target = TargetLDIF()
    target.cli()
