"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container.

REFATORADO COMPLETO:
- REMOVIDA TODAS as duplicações de FlextContainer/DIContainer
- USA APENAS FlextContainer oficial do flext-core
- Mantém apenas utilitários flext_target_ldif-específicos
- SEM fallback, backward compatibility ou código duplicado

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib

# 🚨 ARCHITECTURAL COMPLIANCE: Use ONLY official flext-core FlextContainer
from flext_core import FlextContainer

# ==================== FLEXT_TARGET_LDIF-SPECIFIC DI UTILITIES ====================

_flext_target_ldif_container_instance: FlextContainer | None = None


def get_flext_target_ldif_container() -> FlextContainer:
    """Get FLEXT_TARGET_LDIF-specific DI container instance.

    Returns:
        FlextContainer: Official container from flext-core.

    """
    global _flext_target_ldif_container_instance
    if _flext_target_ldif_container_instance is None:
        _flext_target_ldif_container_instance = FlextContainer()
    return _flext_target_ldif_container_instance


def configure_flext_target_ldif_dependencies() -> None:
    """Configure FLEXT_TARGET_LDIF dependencies using official FlextContainer."""
    get_flext_target_ldif_container()

    with contextlib.suppress(ImportError):
        # Register module-specific dependencies
        # TODO: Add module-specific service registrations here

        # Dependencies configured successfully
        pass


def get_flext_target_ldif_service(service_name: str) -> object:
    """Get flext_target_ldif service from container.

    Args:
        service_name: Name of service to retrieve.

    Returns:
        Service instance or None if not found.

    """
    container = get_flext_target_ldif_container()
    result = container.get(service_name)

    if result.success:
        return result.data

    # Service not found - silent fail for now
    return None


# Initialize flext_target_ldif dependencies on module import
configure_flext_target_ldif_dependencies()
