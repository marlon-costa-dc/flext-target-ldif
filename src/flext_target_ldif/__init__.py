"""FLEXT Target LDIF - Self-contained LDIF target implementation.

This project provides a complete Singer target for LDIF format using flext-core
patterns and flext-ldif infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import flext-core patterns for consistency
from flext_core import FlextError, FlextResult

from flext_target_ldif.config import FlextTargetLdifConfig
from flext_target_ldif.sinks import LDIFSink

# Import local implementations
from flext_target_ldif.target import TargetLDIF
from flext_target_ldif.writer import LdifWriter

# Backward compatibility aliases
FlextLDIFTarget = TargetLDIF
FlextLDIFTargetConfig = FlextTargetLdifConfig
FlextTargetLDIF = TargetLDIF
FlextTargetLDIFConfig = FlextTargetLdifConfig
LDIFTarget = TargetLDIF
TargetLDIFConfig = FlextTargetLdifConfig

__version__ = "0.9.0"

__all__: list[str] = [
    "FlextError",
    # Backward compatibility
    "FlextLDIFTarget",
    "FlextLDIFTargetConfig",
    # Core patterns
    "FlextResult",
    "FlextTargetLDIF",
    "FlextTargetLDIFConfig",
    "FlextTargetLdifConfig",
    "LDIFSink",
    "LDIFTarget",
    "LdifWriter",
    # Main implementation
    "TargetLDIF",
    "TargetLDIFConfig",
    "__version__",
]
