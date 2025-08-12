"""Target client module consolidating main Singer Target and Sink implementations.

Consolidates:
- TargetLDIF (main Singer Target class)
- LDIFSink (Singer Sink implementation)
- LdifWriter (LDIF file writer)
- Complete flext-meltano + flext-ldif integration

Follows established FLEXT patterns:
- Uses flext-core FlextResult for error handling
- Integrates with flext-meltano Target base class
- Leverages flext-ldif infrastructure for LDIF processing
- Eliminates code duplication through composition

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Re-export main target and sink classes for PEP8 consolidation
from flext_target_ldif.sinks import LDIFSink
from flext_target_ldif.target import TargetLDIF
from flext_target_ldif.writer import LdifWriter

# PEP8 descriptive aliases
TargetClient = TargetLDIF
TargetSink = LDIFSink
TargetWriter = LdifWriter

__all__: list[str] = [
    "LDIFSink",
    "LdifWriter",
    "TargetClient",
    "TargetLDIF",
    "TargetSink",
    "TargetWriter",
]
