# FLEXT Target LDIF

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Singer Target](https://img.shields.io/badge/Singer-Target-orange.svg)](https://hub.meltano.com/targets/)
[![FLEXT Framework](https://img.shields.io/badge/FLEXT-Framework-green.svg)](https://github.com/flext-sh/flext)

A Singer-compliant target for outputting data streams to LDAP Data Interchange Format (LDIF) files. Part of the FLEXT enterprise data integration platform.

## Overview

FLEXT Target LDIF converts Singer-formatted data streams into LDIF (LDAP Data Interchange Format) files, enabling data integration workflows that output to LDAP directory systems. The target handles data transformation, DN generation, attribute mapping, and LDIF format compliance.

### Key Features

- **Singer SDK Compliance**: Full compatibility with Singer specification
- **LDIF Format Support**: RFC 2849 compliant LDIF output
- **Flexible DN Generation**: Configurable Distinguished Name templates
- **Attribute Mapping**: Customizable field-to-attribute mapping
- **Data Transformation**: Built-in transformers for common data types
- **FLEXT Integration**: Seamless integration with FLEXT framework
- **Type Safety**: Full type hints and strict MyPy compliance
- **Comprehensive Testing**: 90%+ test coverage with unit and integration tests

## Installation

### From PyPI (Coming Soon)

```bash
pip install flext-target-ldif
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/flext-sh/flext.git
cd flext/flext-target-ldif

# Install with Poetry
make install-dev

# Or install dependencies directly
poetry install --all-extras
```

## Quick Start

### Basic Usage

```bash
# Use with any Singer tap
some-singer-tap | flext-target-ldif --config config.json

# With state file for incremental processing
some-singer-tap | flext-target-ldif --config config.json --state state.json
```

### Configuration

Create a `config.json` file:

```json
{
  "output_path": "./ldif_output",
  "file_naming_pattern": "{stream_name}_{timestamp}.ldif",
  "dn_template": "uid={uid},ou=users,dc=example,dc=com",
  "ldif_options": {
    "line_length": 78,
    "base64_encode": false,
    "include_timestamps": true
  },
  "attribute_mapping": {
    "user_id": "uid",
    "full_name": "cn",
    "email": "mail",
    "first_name": "givenName",
    "last_name": "sn"
  }
}
```

### Example Pipeline

```bash
# Extract users from database and convert to LDIF
tap-postgres --config tap-config.json | flext-target-ldif --config target-config.json
```

## Configuration Reference

### Core Settings

| Setting | Type | Required | Default | Description |
|---------|------|----------|---------|-------------|
| `output_path` | string | No | `"./output"` | Directory for LDIF output files |
| `file_naming_pattern` | string | No | `"{stream_name}_{timestamp}.ldif"` | File naming pattern |
| `dn_template` | string | No | `"uid={uid},ou=users,dc=example,dc=com"` | DN generation template |

### LDIF Options

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `line_length` | integer | `78` | Maximum line length for LDIF |
| `base64_encode` | boolean | `false` | Force base64 encoding for all values |
| `include_timestamps` | boolean | `true` | Include timestamp comments in output |

### Attribute Mapping

Map stream fields to LDAP attributes:

```json
{
  "attribute_mapping": {
    "user_id": "uid",
    "username": "uid", 
    "full_name": "cn",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "phone": "telephoneNumber",
    "title": "title",
    "department": "departmentNumber"
  }
}
```

## LDIF Output Format

### Sample Input (Singer JSON)

```json
{"type": "RECORD", "record": {"uid": "jdoe", "cn": "John Doe", "mail": "john@example.com"}}
```

### Sample Output (LDIF)

```ldif
version: 1
# Generated on: 2025-07-19T12:30:45
# FLEXT Target LDIF - Singer Target

dn: uid=jdoe,ou=users,dc=example,dc=com
uid: jdoe
cn: John Doe
mail: john@example.com
objectClass: inetOrgPerson
objectClass: person

# Total records written: 1
```

## Development

### Development Setup

```bash
# Complete development environment setup
make dev-setup

# Install all dependencies
make install-dev

# Set up pre-commit hooks
poetry run pre-commit install
```

### Quality Assurance

```bash
# Run all quality checks
make check

# Individual checks
make lint          # Ruff linting
make type-check    # MyPy type checking
make security      # Bandit security analysis
make test          # pytest test suite
make test-coverage # Test with coverage report
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test categories
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m ldif              # LDIF-specific tests
pytest -m singer            # Singer-specific tests
```

### Code Formatting

```bash
# Format code with strict standards
make format

# Check formatting without changes
make lint
```

## Meltano Integration

Add to your `meltano.yml`:

```yaml
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
      - name: attribute_mapping
        kind: object
        description: Field to attribute mapping
```

## Advanced Usage

### Custom Transformers

```python
from flext_target_ldif.transformers import RecordTransformer

# Create custom transformer
def custom_phone_transformer(value):
    return f"+1-{value}" if value else ""

custom_transformers = {
    "phone": custom_phone_transformer
}

transformer = RecordTransformer(
    custom_transformers=custom_transformers
)
```

### Programmatic Usage

```python
from flext_target_ldif import TargetLDIF

# Initialize target
config = {
    "output_path": "/path/to/output",
    "dn_template": "uid={uid},ou=users,dc=example,dc=com"
}

target = TargetLDIF(config=config)

# Process records
# (typically done via Singer protocol)
```

## Architecture

### Component Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Singer Tap    │───▶│  FLEXT Target    │───▶│   LDIF Files    │
│                 │    │      LDIF        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ FLEXT Framework  │
                    │   (Core + Obs)   │
                    └──────────────────┘
```

### Key Components

- **TargetLDIF**: Main Singer target implementation
- **LDIFSink**: Stream-specific sink for LDIF output
- **LDIFWriter**: Core LDIF format writing logic
- **RecordTransformer**: Data transformation utilities
- **Validation**: Input validation and schema checking

## LDAP Integration

### Importing LDIF Files

```bash
# OpenLDAP
ldapadd -x -D "cn=admin,dc=example,dc=com" -W -f users.ldif

# Active Directory
ldifde -i -f users.ldif -s server.example.com

# 389 Directory Server
ldapmodify -x -D "cn=Directory Manager" -W -f users.ldif
```

### ObjectClass Mapping

The target automatically adds required objectClass attributes:

- `inetOrgPerson` - For user entries with email, names
- `person` - Base person objectClass
- Custom objectClass can be specified via attribute mapping

## Troubleshooting

### Common Issues

**Import Errors**

```bash
# Ensure virtual environment is activated
poetry shell
# Or set PYTHONPATH
export PYTHONPATH=/path/to/flext/flext-target-ldif/src:$PYTHONPATH
```

**Configuration Validation Errors**

```bash
# Enable debug logging
FLEXT_TARGET_LDIF_DEBUG=true flext-target-ldif --config config.json
```

**LDIF Format Issues**

- Check line length settings (default: 78 characters)
- Verify DN template has required variables
- Ensure attribute names are LDAP-compliant

**Performance Optimization**

- Use streaming for large datasets
- Adjust line length for faster processing
- Consider compression for large outputs

### Debug Mode

Enable detailed logging:

```bash
# Environment variable
export FLEXT_TARGET_LDIF_DEBUG=true

# Or in config
{
  "debug": true,
  "output_path": "./debug_output"
}
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run quality checks: `make check`
5. Submit a pull request

### Code Standards

- Python 3.13+ required
- Type hints for all code
- 90%+ test coverage
- Ruff linting compliance
- MyPy strict mode

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [FLEXT Docs](https://docs.flext.sh)
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Discussions**: [GitHub Discussions](https://github.com/flext-sh/flext/discussions)

## Related Projects

- [FLEXT Core](../flext-core/) - Core framework libraries
- [FLEXT Observability](../flext-observability/) - Monitoring and logging
- [Singer SDK](https://github.com/MeltanoLabs/sdk) - Singer development framework
- [Meltano](https://meltano.com/) - Data integration platform

---

**FLEXT Target LDIF** is part of the [FLEXT Framework](https://github.com/flext-sh/flext) - Enterprise Data Integration Platform.
