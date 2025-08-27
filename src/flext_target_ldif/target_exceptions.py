"""Target exceptions module using flext-core factory patterns.

Consolidates all LDIF target exception classes:
- Domain-specific exceptions with structured error details
- Factory pattern to eliminate code duplication
- Integration with flext-core exception hierarchy
- Railway-oriented programming support

Follows established FLEXT patterns:
- Uses flext-core FlextExceptions base classes
- Structured error context with FlextValue
- Type-safe exception handling
- Comprehensive error categorization

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export exception classes for PEP8 consolidation
from flext_target_ldif.exceptions import (
    FlextTargetLdifError,
    FlextTargetLdifErrorDetails,
    FlextTargetLdifFileError,
    FlextTargetLdifInfrastructureError,
    FlextTargetLdifSchemaError,
    FlextTargetLdifTransformationError,
    FlextTargetLdifWriterError,
)

# PEP8 descriptive aliases
TargetError = FlextTargetLdifError
TargetWriterError = FlextTargetLdifWriterError
TargetTransformationError = FlextTargetLdifTransformationError
TargetFileError = FlextTargetLdifFileError
TargetSchemaError = FlextTargetLdifSchemaError
TargetInfrastructureError = FlextTargetLdifInfrastructureError
TargetErrorDetails = FlextTargetLdifErrorDetails

__all__: list[str] = [
    "FlextTargetLdifError",
    "FlextTargetLdifErrorDetails",
    "FlextTargetLdifFileError",
    "FlextTargetLdifInfrastructureError",
    "FlextTargetLdifSchemaError",
    "FlextTargetLdifTransformationError",
    "FlextTargetLdifWriterError",
    "TargetError",
    "TargetErrorDetails",
    "TargetFileError",
    "TargetInfrastructureError",
    "TargetSchemaError",
    "TargetTransformationError",
    "TargetWriterError",
]
