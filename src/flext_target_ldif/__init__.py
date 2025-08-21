"""Enterprise Singer Target for LDIF data export."""

from __future__ import annotations

import importlib.metadata

# flext-core imports
from flext_core import FlextError, FlextResult, FlextValue, get_logger

# === FLEXT-MELTANO COMPLETE INTEGRATION ===
# Re-export ALL flext-meltano facilities for full ecosystem integration
from flext_meltano import (
    BatchSink,
    FlextMeltanoBaseService,
    # Bridge integration
    FlextMeltanoBridge,
    # Configuration and validation
    FlextMeltanoConfig,
    FlextMeltanoEvent,
    # RESTStream,  # Not in flext_meltano yet
    # Enterprise services from flext-meltano.base
    FlextMeltanoTargetService,
    # Authentication patterns
    OAuthAuthenticator,
    # Typing definitions
    PropertiesList,
    Property,
    Sink,
    SQLSink,
    # Core Singer SDK classes (centralized from flext-meltano)
    Stream,
    Tap,
    Target,
    create_meltano_target_service,
    # Testing utilities
    get_tap_test_class,  # Using tap test class for targets too
    # Singer typing utilities (centralized)
    singer_typing,
)

# === PEP8 CONSOLIDATED MODULE IMPORTS ===
# Import from consolidated PEP8 modules for better organization
from flext_target_ldif.target_client import (
    LDIFSink,
    LdifWriter,
    TargetClient,
    TargetLDIF,
    TargetSink,
    TargetWriter,
)
from flext_target_ldif.target_config import FlextTargetLdifConfig, TargetConfig
from flext_target_ldif.target_exceptions import (
    FlextTargetLdifError,
    FlextTargetLdifErrorDetails,
    FlextTargetLdifFileError,
    FlextTargetLdifInfrastructureError,
    FlextTargetLdifSchemaError,
    FlextTargetLdifTransformationError,
    FlextTargetLdifWriterError,
    TargetError,
    TargetErrorDetails,
    TargetFileError,
    TargetInfrastructureError,
    TargetSchemaError,
    TargetTransformationError,
    TargetWriterError,
)
from flext_target_ldif.models import (
    RecordTransformer,
    TargetTransformer,
    TargetValidator,
    ValidationError,
    normalize_attribute_value,
    sanitize_attribute_name,
    transform_boolean,
    transform_email,
    transform_name,
    transform_phone,
    transform_timestamp,
    validate_attribute_name,
    validate_attribute_value,
    validate_dn_component,
    validate_record,
    validate_schema,
)
from flext_target_ldif.target_services import (
    TargetCLI,
    TargetContainer,
    TargetService,
    cli_main,
    config_target_dependencies,
    configure_flext_target_ldif_dependencies,
    get_flext_target_ldif_container,
    get_flext_target_ldif_service,
)

# === BACKWARD COMPATIBILITY IMPORTS ===
# Direct imports for existing code compatibility
from flext_target_ldif.config import FlextTargetLdifConfig as _FlextTargetLdifConfig
from flext_target_ldif.sinks import LDIFSink as _LDIFSink
from flext_target_ldif.target import TargetLDIF as _TargetLDIF
from flext_target_ldif.writer import LdifWriter as _LdifWriter

# === BACKWARD COMPATIBILITY ALIASES ===
# Ensure all existing code continues to work
FlextLDIFTarget = _TargetLDIF
FlextLDIFTargetConfig = _FlextTargetLdifConfig
FlextTargetLDIF = _TargetLDIF
FlextTargetLDIFConfig = _FlextTargetLdifConfig
LDIFTarget = _TargetLDIF
TargetLDIFConfig = _FlextTargetLdifConfig

# FlextTargetLdifConfig already imported from target_config module above

# Version following semantic versioning
try:
    __version__ = importlib.metadata.version("flext-target-ldif")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.9.0-enterprise"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Complete public API exports with PEP8 consolidation and backward compatibility
__all__: list[str] = [
    # === FLEXT-MELTANO RE-EXPORTS ===
    "BatchSink",
    "FlextMeltanoBaseService",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoEvent",
    "FlextMeltanoTargetService",
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "SQLSink",
    "Sink",
    "Stream",
    "Tap",
    "Target",
    "create_meltano_target_service",
    "get_tap_test_class",
    "singer_typing",
    # === FLEXT-CORE RE-EXPORTS ===
    "FlextError",
    "FlextResult",
    "FlextValue",
    "get_logger",
    # === PEP8 CONSOLIDATED MODULES (Primary Interface) ===
    # Configuration
    "FlextTargetLdifConfig",
    "TargetConfig",
    # Client (Target + Sink + Writer)
    "LDIFSink",
    "LdifWriter",
    "TargetClient",
    "TargetLDIF",
    "TargetSink",
    "TargetWriter",
    # Models (Validation + Transformation)
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
    # Exceptions
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
    # Services (DI + CLI)
    "TargetCLI",
    "TargetContainer",
    "TargetService",
    "cli_main",
    "config_target_dependencies",
    "configure_flext_target_ldif_dependencies",
    "get_flext_target_ldif_container",
    "get_flext_target_ldif_service",
    # === BACKWARD COMPATIBILITY ALIASES ===
    "FlextLDIFTarget",
    "FlextLDIFTargetConfig",
    "FlextTargetLDIF",
    "FlextTargetLDIFConfig",
    "LDIFTarget",
    "TargetLDIFConfig",
    # === METADATA ===
    "__version__",
    "__version_info__",
]
