"""Target models module for LDIF data structures.

Consolidates LDIF-specific data models and transformations:
- Record validation and transformation logic
- LDAP attribute mapping and normalization
- Schema validation for Singer streams
- Integration with flext-ldap utilities

Follows established FLEXT patterns:
- Uses flext-core FlextValueObject for data models
- Leverages flext-ldap infrastructure to eliminate duplication
- Type-safe transformations with comprehensive validation
- Railway-oriented programming with FlextResult

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export transformation and validation utilities for PEP8 consolidation
from flext_target_ldif.transformers import (
    RecordTransformer,
    normalize_attribute_value,
    transform_boolean,
    transform_email,
    transform_name,
    transform_phone,
    transform_timestamp,
)
from flext_target_ldif.validation import (
    ValidationError,
    sanitize_attribute_name,
    validate_attribute_name,
    validate_attribute_value,
    validate_dn_component,
    validate_record,
    validate_schema,
)

# PEP8 descriptive aliases
TargetTransformer = RecordTransformer
TargetValidator = validate_record

__all__: list[str] = [
    "RecordTransformer",
    "TargetTransformer",
    "TargetValidator",
    "ValidationError",
    "normalize_attribute_value",
    "sanitize_attribute_name",
    "transform_boolean",
    "transform_email",
    "transform_name",
    "transform_phone",
    "transform_timestamp",
    "validate_attribute_name",
    "validate_attribute_value",
    "validate_dn_component",
    "validate_record",
    "validate_schema",
]
