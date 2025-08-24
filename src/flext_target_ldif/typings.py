"""Centralized typings facade for flext-target-ldif.

- Extends flext-core types
- Add Target LDIF-specific type aliases and Protocols here
"""

from __future__ import annotations

from flext_core import E, F, FlextTypes as CoreFlextTypes, P, R, T, U, V


class FlextTypes(CoreFlextTypes):
    """Target LDIF domain-specific types can extend here."""


__all__ = [
    "E",
    "F",
    "FlextTypes",
    "P",
    "R",
    "T",
    "U",
    "V",
]
