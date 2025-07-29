"""FLEXT Target LDIF - Wrapper for flext-meltano consolidated implementation.

CONSOLIDATION: This project is now a library wrapper that imports the real
Singer/Meltano/DBT consolidated implementations from flext-meltano to eliminate
code duplication across the FLEXT ecosystem.

This follows the architectural principle:
- flext-* projects are LIBRARIES, not services
- tap/target/dbt/ext are Meltano plugins
- Real implementations are in flext-meltano

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import flext-core patterns for consistency
from flext_core import FlextError, FlextResult

# Import consolidated implementations from flext-meltano
# MIGRATED: Singer SDK imports centralized via flext-meltano
from flext_meltano.targets.ldif import (
    FlextLDIFTarget,
    FlextLDIFTargetConfig,
    TargetLDIF,
    TargetLDIFConfig,
)

# Backward compatibility aliases
FlextTargetLDIF = FlextLDIFTarget
FlextTargetLDIFConfig = FlextLDIFTargetConfig
LDIFTarget = TargetLDIF

__version__ = "0.8.0"

__all__ = [
    # Main implementation (from flext-meltano)
    "FlextLDIFTarget",
    "FlextLDIFTargetConfig",
    # Core patterns
    "FlextResult",
    # Backward compatibility
    "FlextTargetLDIF",
    "FlextTargetLDIFConfig",
    "LDIFTarget",
    "TargetLDIF",
    "TargetLDIFConfig",
    "__version__",
]
