"""Target configuration module for FLEXT Target LDIF.

Provides comprehensive configuration management following flext-core patterns:
- FlextValue base class for type safety
- Business rule validation with FlextResult
- Integration with flext-ldap for DN validation
- Eliminates code duplication through composition

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

# Re-export from config module for PEP8 consolidation
from flext_target_ldif.config import FlextTargetLdifConfig

# PEP8 descriptive alias
TargetConfig = FlextTargetLdifConfig

__all__: list[str] = [
    "FlextTargetLdifConfig",
    "TargetConfig",
]
