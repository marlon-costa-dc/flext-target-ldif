"""Version information for flext-target-ldif package.

This module contains version information for the flext-target-ldif package.
"""

from __future__ import annotations

import importlib.metadata

# Simple version implementation for architectural compliance
try:
    __version__ = importlib.metadata.version("flext-target-ldif")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.7.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())
