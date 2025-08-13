"""Compatibility facade: re-export target_models via models.py.

Standardizes imports to use flext_target_ldif.models across the codebase.
"""

from __future__ import annotations

from .target_models import *  # noqa: F403
