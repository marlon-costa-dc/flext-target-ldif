"""Target services module for dependency injection and CLI utilities.

Consolidates service-oriented components:
- Dependency injection container management
- CLI entry point and utilities
- Service orchestration patterns
- Integration with flext-core container

Follows established FLEXT patterns:
- Uses flext-core FlextContainer for dependency injection
- Eliminates duplicate container implementations
- Type-safe service resolution
- Centralized service configuration

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export service utilities for PEP8 consolidation
from flext_target_ldif.cli import main as cli_main
from flext_target_ldif.di_container import (
    configure_flext_target_ldif_dependencies,
    get_flext_target_ldif_container,
    get_flext_target_ldif_service,
)

# PEP8 descriptive aliases
TargetCLI = cli_main
TargetContainer = get_flext_target_ldif_container
TargetService = get_flext_target_ldif_service
config_target_dependencies = configure_flext_target_ldif_dependencies

__all__: list[str] = [
    "TargetCLI",
    "TargetContainer",
    "TargetService",
    "cli_main",
    "config_target_dependencies",
    "configure_flext_target_ldif_dependencies",
    "get_flext_target_ldif_container",
    "get_flext_target_ldif_service",
]
