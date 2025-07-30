# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**flext-target-ldif** is a Singer-compliant target for exporting data to LDIF (LDAP Data Interchange Format) files. It's part of the FLEXT enterprise data integration ecosystem and provides high-performance LDIF file generation with comprehensive validation and type safety.

## Architecture

### Core Components

- **TargetLDIF** (`target.py`): Main Singer target implementation using the flext-meltano framework
- **LDIFSink** (`sinks.py`): Singer sink for processing records and batching writes
- **LdifWriter** (`writer.py`): Core LDIF file writer using flext-ldif infrastructure
- **FlextTargetLdifConfig** (`config.py`): Configuration classes with validation using flext-core patterns

### Technology Stack

- **Python 3.13**: Latest Python with strict type checking
- **Singer SDK**: Data integration protocol via flext-meltano
- **FLEXT Core**: Foundation patterns (FlextResult, FlextValueObject, dependency injection)
- **FLEXT LDIF**: Specialized LDIF processing infrastructure
- **Pydantic**: Configuration validation and data modeling

### Dependencies

The project integrates with the FLEXT ecosystem:
- `flext-core`: Base patterns and utilities
- `flext-meltano`: Singer SDK integration
- `flext-ldif`: LDIF processing infrastructure  
- `flext-observability`: Monitoring and logging

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation - all must pass
make validate               # lint + type-check + security + test (90% coverage)

# Essential quality checks
make check                  # lint + type-check + test

# Individual quality gates
make lint                   # Ruff linting (ALL rules enabled)  
make type-check            # MyPy strict mode type checking
make security              # Bandit + pip-audit + secrets scan
make test                  # Pytest with 90% coverage requirement
```

### Testing Commands

```bash
# Comprehensive testing
make test                   # All tests with coverage report
make test-unit             # Unit tests only  
make test-integration      # Integration tests only
make test-singer           # Singer protocol tests
make coverage              # Generate HTML coverage report

# Test with specific markers
pytest -m unit             # Unit tests only
pytest -m integration      # Integration tests only
pytest -m ldif             # LDIF-specific tests
pytest -m singer           # Singer protocol tests
pytest -m slow             # Slow running tests
```

### Singer Target Operations

```bash
# Target functionality
make target-test           # Test basic target functionality
make target-validate       # Validate target configuration
make target-schema         # Validate LDIF schema
make target-run            # Run LDIF data export with test data
make target-run-debug      # Run with debug logging
make target-dry-run        # Run in dry-run mode

# Singer protocol commands
make singer-about          # Show target information
make singer-config-sample  # Generate configuration sample
```

### LDIF-Specific Operations

```bash
# LDIF file operations
make ldif-write            # Test LDIF writing functionality
make ldif-validate-output  # Validate LDIF output format
make ldif-format-check     # Check LDIF format compliance
make ldif-export-users     # Export user data to LDIF
make ldif-export-groups    # Export group data to LDIF

# LDIF processing
make ldif-merge            # Merge multiple LDIF files
make ldif-split            # Split LDIF file by entry type
make ldif-clean            # Clean and normalize LDIF output
```

### Development Setup

```bash
# Complete development setup
make setup                 # install + pre-commit hooks

# Installation
make install               # Install all dependencies
make dev-install           # Development mode with pre-commit
make pre-commit            # Setup pre-commit hooks

# Code formatting
make format                # Format code with ruff
make fix                   # Auto-fix formatting and lint issues
```

### Dependency Management

```bash
# Dependency operations
make deps-update           # Update all dependencies
make deps-audit            # Security audit of dependencies
make deps-tree             # Show dependency tree
make deps-outdated         # Show outdated dependencies
```

## Configuration

### Target Configuration Schema

```json
{
  "output_path": "./output",
  "file_naming_pattern": "{stream_name}_{timestamp}.ldif",
  "dn_template": "uid={uid},ou=users,dc=example,dc=com",
  "attribute_mapping": {
    "user_id": "uid",
    "full_name": "cn",
    "email": "mail"
  },
  "ldif_options": {
    "line_length": 78,
    "base64_encode": false,
    "include_timestamps": true
  }
}
```

### Running the Target

```bash
# Basic usage
target-ldif --config config.json < input.jsonl

# With debug logging
target-ldif --config config.json --log-level DEBUG < input.jsonl

# Dry run mode
target-ldif --config config.json --dry-run < input.jsonl

# Using command line
echo '{"uid":"test","cn":"Test User"}' | target-ldif --config config.json
```

## Code Quality Standards

### Zero Tolerance Quality Gates

- **Coverage**: Minimum 90% test coverage required
- **Type Safety**: Strict MyPy configuration with zero errors
- **Linting**: Ruff with ALL rule categories enabled
- **Security**: Bandit security scanning and pip-audit vulnerability checks
- **Pre-commit**: Automated quality checks on every commit

### Testing Strategy

- **Unit Tests**: Core functionality with mocks and fixtures
- **Integration Tests**: End-to-end LDIF file generation
- **Singer Tests**: Protocol compliance verification
- **LDIF Tests**: Format validation and schema compliance

### Architecture Patterns

- **FlextResult**: Railway-oriented programming for error handling
- **FlextValueObject**: Domain modeling with validation
- **Dependency Injection**: Using flext-core DI container
- **Clean Architecture**: Clear separation of concerns

## File Structure

```
src/flext_target_ldif/
├── __init__.py           # Package initialization
├── target.py             # Main Singer target implementation
├── sinks.py              # Singer sink for batch processing
├── writer.py             # LDIF file writer using flext-ldif
├── config.py             # Configuration classes with validation
├── exceptions.py         # Custom exception classes
├── validation.py         # Input validation logic
├── transformers.py       # Data transformation utilities
├── cli.py                # Command-line interface
└── infrastructure/       # Infrastructure layer
    ├── __init__.py
    └── di_container.py   # Dependency injection setup

tests/
├── conftest.py           # Pytest configuration and fixtures
├── test_target.py        # Target implementation tests
├── test_writer.py        # LDIF writer tests
└── test_exceptions.py    # Exception handling tests
```

## Development Workflow

1. **Setup**: Run `make setup` for complete development environment
2. **Development**: Use `make check` frequently during development
3. **Testing**: Run `make test` to ensure coverage requirements
4. **Quality**: Run `make validate` before committing (required to pass)
5. **Integration**: Test Singer protocol with `make target-test`

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: LDIF Library Integration Efficiency
**Status**: ALTO - Integration com flext-ldif pode ser optimized
**Problema**:
- LdifWriter usando flext-ldif infrastructure mas pode duplicate functionality
- LDIF processing patterns podem divergir entre target e library
- Performance optimization opportunities podem não be leveraged

**TODO**:
- [ ] Optimize integration com flext-ldif para eliminate duplication
- [ ] Leverage advanced LDIF processing features from library
- [ ] Align LDIF validation patterns
- [ ] Document LDIF integration best practices

### 🚨 GAP 2: Singer Target Data Loading Patterns
**Status**: ALTO - LDIF target loading patterns podem não be optimal
**Problema**:
- Batch processing strategies para LDIF não documented
- Memory management para large LDIF exports pode be issue
- Error handling para LDIF format errors pode be incomplete

**TODO**:
- [ ] Implement LDIF batch processing optimizations
- [ ] Add memory-efficient streaming para large exports
- [ ] Enhance error handling para LDIF-specific failures
- [ ] Document LDIF target loading patterns

### 🚨 GAP 3: LDIF Format Validation Completeness
**Status**: ALTO - LDIF format validation pode não be comprehensive
**Problema**:
- LDIF format compliance validation pode be incomplete
- Schema validation para LDIF attributes pode be missing
- Data quality checks específicos para LDIF podem be needed

**TODO**:
- [ ] Implement comprehensive LDIF format validation
- [ ] Add schema-aware LDIF validation
- [ ] Include data quality checks específicos para LDIF
- [ ] Document LDIF validation strategies

## Environment Variables

```bash
# Python settings
PYTHON=python3.13
PYTHONPATH=src
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1

# Singer settings
SINGER_LOG_LEVEL=INFO
SINGER_BATCH_SIZE=100
SINGER_MAX_BATCH_AGE=300

# LDIF Target settings
TARGET_LDIF_OUTPUT_DIR=output
TARGET_LDIF_FILENAME=export.ldif
TARGET_LDIF_ENCODING=utf-8
TARGET_LDIF_LINE_LENGTH=76
TARGET_LDIF_VALIDATE_FORMAT=true
TARGET_LDIF_INCLUDE_COMMENTS=false
TARGET_LDIF_SORT_ENTRIES=true
```

## Troubleshooting

### Common Issues

**LDIF Format Errors**: Use `make ldif-validate-output` to check format compliance

**Configuration Issues**: Run `make target-validate` to verify configuration

**Performance Issues**: Check batch size and memory usage with debug logging

**Test Failures**: Use `pytest --lf` to run only failed tests for quick feedback

### Debugging

```bash
# Debug target execution
make target-run-debug

# Run tests with verbose output
pytest -v -s

# Check specific test markers
pytest -m ldif -v
```