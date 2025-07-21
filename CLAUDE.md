# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

FLEXT Target LDIF is a Singer-compliant target for outputting LDAP Data Interchange Format (LDIF) files. This project is part of the larger FLEXT enterprise data integration platform and implements the Singer specification for handling data streams and converting them to LDIF format for LDAP directory operations.

## Development Commands

### Local Commands (run from this directory)

```bash
# Installation and setup
make install               # Install dependencies with Poetry
make install-dev           # Install with dev dependencies
make dev-setup             # Complete development environment setup

# Quality checks (ALWAYS run before committing)
make check                 # Run all quality checks (lint + type + security + test)
make lint                  # Run linting with Ruff (strict configuration)
make type-check            # Run MyPy type checking (strict mode)
make security              # Run Bandit security analysis
make test                  # Run pytest test suite
make test-coverage         # Run tests with coverage reporting

# Development workflow
make format                # Format code with Black and Ruff
make dev                   # Run target in development mode
make dev-test              # Quick development test cycle
make pre-commit            # Run pre-commit hooks

# Build and packaging
make build                 # Build package with Poetry
make clean                 # Clean build artifacts
```

### Workspace Commands (run from `/home/marlonsc/flext/`)

```bash
# Multi-project commands that include this target
make check-all             # Run quality checks on all projects including this one
make test-all              # Run tests across all projects
make sync-deps             # Sync dependencies across workspace projects
```

## Architecture

### Singer Target Implementation

This project implements the Singer target specification:

- **Input**: Singer-formatted JSON messages via stdin
- **Output**: LDIF (LDAP Data Interchange Format) files
- **Configuration**: JSON-based configuration following Singer conventions
- **State**: Singer state management for incremental processing

### Project Structure

```
src/flext_target_ldif/     # Main source code
├── __init__.py           # Package initialization
├── target.py             # Main target implementation (TargetLDIF class)
├── sinks.py              # LDIF sink implementations
├── ldif_writer.py        # LDIF format writing logic
├── transformers.py       # Data transformation utilities
├── validation.py         # Input data validation
└── config.py             # Configuration management

tests/                    # Test suite
├── __init__.py
├── test_target.py        # Main target tests
├── test_sinks.py         # Sink functionality tests
├── test_ldif_writer.py   # LDIF writing tests
├── test_transformers.py  # Data transformation tests
└── fixtures/             # Test data and fixtures
```

### Key Components

1. **TargetLDIF**: Main Singer target class inheriting from Singer SDK
2. **LDIF Sinks**: Stream handlers that write data to LDIF format
3. **LDIF Writer**: Core component for generating valid LDIF output
4. **Transformers**: Data transformation and schema mapping utilities
5. **Validators**: Input validation and schema checking

## Technology Stack

### Core Dependencies

- **Python 3.13**: Required Python version (workspace standard)
- **Singer SDK**: Foundation for Singer target implementation
- **FLEXT Core**: Shared utilities and base classes from the FLEXT framework
- **FLEXT Observability**: Logging, metrics, and monitoring integration

### LDIF-Specific Dependencies

- **Standard Library**: Uses Python's built-in string and file handling for LDIF generation
- **Pydantic**: Data validation and settings management (via FLEXT Core)
- **Structlog**: Structured logging (via FLEXT Observability)

### Development Tools

- **Poetry**: Dependency management and packaging
- **Ruff**: Linting with strict Singer target configuration
- **MyPy**: Type checking in strict mode
- **pytest**: Testing framework with coverage reporting
- **Black**: Code formatting
- **Bandit**: Security analysis

## Configuration

### Target Configuration Schema

```json
{
  "output_path": "string",          # Directory for LDIF output files
  "file_naming_pattern": "string",  # Pattern for LDIF file names
  "ldif_options": {
    "line_length": "integer",       # Maximum line length for LDIF
    "base64_encode": "boolean",     # Force base64 encoding for values
    "include_timestamps": "boolean" # Add timestamp comments
  },
  "dn_template": "string",         # Template for generating DN attributes
  "attribute_mapping": "object"    # Mapping of stream fields to LDAP attributes
}
```

### Environment Variables

- `FLEXT_TARGET_LDIF_CONFIG`: Path to configuration file
- `FLEXT_TARGET_LDIF_OUTPUT_PATH`: Default output directory
- `FLEXT_TARGET_LDIF_DEBUG`: Enable debug logging
- `PYTHONPATH`: Must include `src` directory for development

## Usage Patterns

### Singer Target Usage

```bash
# Basic usage with singer-io tap
some-singer-tap | flext-target-ldif --config config.json

# With state file for incremental processing
some-singer-tap | flext-target-ldif --config config.json --state state.json

# Development usage with debug output
FLEXT_TARGET_LDIF_DEBUG=true flext-target-ldif --config config.json < input.jsonl
```

### Meltano Integration

```yaml
# meltano.yml configuration
targets:
  - name: target-ldif
    namespace: flext_target_ldif
    pip_url: flext-target-ldif
    settings:
      - name: output_path
        kind: string
        description: Output directory for LDIF files
      - name: dn_template
        kind: string  
        description: Template for DN generation
```

## Testing

### Test Structure

- **Unit Tests**: Test individual components (sinks, writers, transformers)
- **Integration Tests**: Test complete Singer target functionality
- **Schema Tests**: Validate LDIF output format compliance
- **Fixture Tests**: Use real-world data samples for validation

### Coverage Requirements

- Minimum 90% test coverage (enforced by pytest configuration)
- All public APIs must have tests
- All error conditions must be tested
- LDIF output format must be validated

## Code Quality Standards

### Linting Configuration

- Ruff with ALL rules enabled and Singer-specific exceptions
- Strict type checking with MyPy
- Security analysis with Bandit
- Pre-commit hooks for consistent quality

### Singer Target Specific Rules

- Use Singer SDK base classes and patterns
- Follow Singer specification for message handling
- Implement proper state management for incremental processing
- Handle Singer SCHEMA, RECORD, and STATE messages correctly
- Provide comprehensive error handling and logging

## Development Guidelines

### Adding New Features

1. Understand Singer specification requirements
2. Update configuration schema if needed
3. Implement with proper error handling
4. Add comprehensive tests including edge cases
5. Update documentation and examples
6. Verify LDIF output format compliance

### LDIF Format Compliance

- Follow RFC 2849 LDIF specification
- Handle special characters and encoding correctly
- Generate valid Distinguished Names (DNs)
- Support proper line wrapping and base64 encoding
- Include appropriate LDIF headers and comments

### Integration with FLEXT Framework

- Use FLEXT Core utilities for common functionality
- Follow FLEXT logging patterns via FLEXT Observability
- Maintain compatibility with workspace tooling
- Use shared configuration patterns where applicable

## Troubleshooting

### Common Issues

- **Import Errors**: Ensure `PYTHONPATH` includes `src` directory
- **Configuration Errors**: Validate JSON schema and required fields
- **LDIF Format Issues**: Check line length and encoding settings
- **Permission Errors**: Verify write access to output directory

### Debug Mode

Enable debug logging with `FLEXT_TARGET_LDIF_DEBUG=true` for detailed output including:
- Singer message processing
- LDIF generation steps  
- File writing operations
- Configuration validation

### Performance Optimization

- Use streaming LDIF writing for large datasets
- Implement batch processing for multiple records
- Monitor memory usage for large attribute values
- Consider compression for large LDIF outputs