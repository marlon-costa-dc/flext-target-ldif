"""FLEXT TARGET LDIF - Singer LDIF Output with simplified imports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Version 0.7.0 - Singer LDIF Target with simplified public API:
- All common imports available from root: from flext_target_ldif import TargetLDIF
- Built on flext-core foundation for robust LDIF generation
- Deprecation warnings for internal imports
"""

from __future__ import annotations

import contextlib
import importlib.metadata
import warnings

# Import from flext-core for foundational patterns
from flext_core import BaseConfig, DomainBaseModel
from flext_core.domain.shared_types import ServiceResult

try:
    __version__ = importlib.metadata.version("flext-target-ldif")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())


class FlextTargetLDIFDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT TARGET LDIF import changes."""


def _show_deprecation_warning(old_import: str, new_import: str) -> None:
    """Show deprecation warning for import paths."""
    message_parts = [
        f"⚠️  DEPRECATED IMPORT: {old_import}",
        f"✅ USE INSTEAD: {new_import}",
        "🔗 This will be removed in version 1.0.0",
        "📖 See FLEXT TARGET LDIF docs for migration guide",
    ]
    warnings.warn(
        "\n".join(message_parts),
        FlextTargetLDIFDeprecationWarning,
        stacklevel=3,
    )


# ================================
# SIMPLIFIED PUBLIC API EXPORTS
# ================================

# Foundation patterns - ALWAYS from flext-core
from flext_core import (
    BaseConfig as LDIFBaseConfig,  # Configuration base
    DomainBaseModel as BaseModel,  # Base for LDIF models
    DomainError as LDIFError,  # LDIF-specific errors
    ServiceResult as ServiceResult,  # LDIF operation results
    ValidationError as ValidationError,  # Validation errors
)

# Singer Target exports - simplified imports
try:
    from flext_target_ldif.target import TargetLDIF
except ImportError:
    # Target not yet fully refactored - provide placeholder
    TargetLDIF = None

# LDIF Writer exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_ldif.ldif_writer import LDIFWriter

# LDIF Sinks exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_ldif.sinks import LDIFSink

# LDIF Transformers exports - simplified imports
with contextlib.suppress(ImportError):
    from flext_target_ldif.transformers import (
        LDIFTransformer,
        RecordTransformer,
    )

# ================================
# PUBLIC API EXPORTS
# ================================

__all__ = [
    "BaseModel",  # from flext_target_ldif import BaseModel
    # Deprecation utilities
    "FlextTargetLDIFDeprecationWarning",
    # Core Patterns (from flext-core)
    "LDIFBaseConfig",  # from flext_target_ldif import LDIFBaseConfig
    "LDIFError",  # from flext_target_ldif import LDIFError
    # LDIF Components (simplified access)
    "LDIFSink",  # from flext_target_ldif import LDIFSink
    "LDIFTransformer",  # from flext_target_ldif import LDIFTransformer
    "LDIFWriter",  # from flext_target_ldif import LDIFWriter
    "RecordTransformer",  # from flext_target_ldif import RecordTransformer
    "ServiceResult",  # from flext_target_ldif import ServiceResult
    # Main Singer Target (simplified access)
    "TargetLDIF",  # from flext_target_ldif import TargetLDIF
    "ValidationError",  # from flext_target_ldif import ValidationError
    # Version
    "__version__",
    "__version_info__",
]
