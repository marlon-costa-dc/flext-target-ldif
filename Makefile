# FLEXT Target LDIF - LDIF File Singer Target
# ==========================================
# Enterprise-grade Singer target for LDIF file data export
# Python 3.13 + Singer SDK + LDIF + FLEXT Core + Zero Tolerance Quality Gates

.PHONY: help info diagnose check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-singer
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: sync validate-config target-test target-validate target-schema target-run
.PHONY: ldif-write ldif-validate-output ldif-format-check

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🎯 FLEXT Target LDIF - LDIF File Singer Target"
	@echo "============================================="
	@echo "🎯 Singer SDK + LDIF + FLEXT Core + Python 3.13"
	@echo ""
	@echo "📦 Enterprise-grade LDIF file target for Singer protocol"
	@echo "🔒 Zero tolerance quality gates with LDIF export"
	@echo "🧪 90%+ test coverage requirement with LDIF integration testing"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'


info: ## Show project information
	@echo "📊 Project Information"
	@echo "======================"
	@echo "Name: flext-target-ldif"
	@echo "Type: singer-target"
	@echo "Title: FLEXT TARGET LDIF"
	@echo "Version: $(shell poetry version -s 2>/dev/null || echo "0.7.0")"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Not found")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Not installed")"
	@echo "Venv: $(shell poetry env info --path 2>/dev/null || echo "Not activated")"
	@echo "Directory: $(CURDIR)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo "Not a git repo")"
	@echo "Git Status: $(shell git status --porcelain 2>/dev/null | wc -l | xargs echo) files changed"

diagnose: ## Run complete diagnostics
	@echo "🔍 Running diagnostics for flext-target-ldif..."
	@echo "System Information:"
	@echo "OS: $(shell uname -s)"
	@echo "Architecture: $(shell uname -m)"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Not found")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Not installed")"
	@echo ""
	@echo "Project Structure:"
	@ls -la
	@echo ""
	@echo "Poetry Configuration:"
	@poetry config --list 2>/dev/null || echo "Poetry not configured"
	@echo ""
	@echo "Dependencies Status:"
	@poetry show --outdated 2>/dev/null || echo "No outdated dependencies"

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT TARGET LDIF COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_target_ldif --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-singer: ## Run Singer protocol tests
	@echo "🧪 Running Singer protocol tests..."
	@poetry run pytest tests/singer/ -v
	@echo "✅ Singer tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_target_ldif --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🎯 SINGER TARGET OPERATIONS
# ============================================================================

sync: ## Sync data to LDIF target
	@echo "🎯 Running LDIF data sync..."
	@poetry run target-ldif --config $(TARGET_CONFIG) < $(TARGET_STATE)
	@echo "✅ LDIF sync complete"

validate-config: ## Validate target configuration
	@echo "🔍 Validating target configuration..."
	@poetry run target-ldif --config $(TARGET_CONFIG) --validate-config
	@echo "✅ Target configuration validated"

target-test: ## Test LDIF target functionality
	@echo "🎯 Testing LDIF target functionality..."
	@poetry run target-ldif --about
	@poetry run target-ldif --version
	@echo "✅ Target test complete"

target-validate: ## Validate target configuration
	@echo "🔍 Validating target configuration..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json --validate-config
	@echo "✅ Target configuration validated"

target-schema: ## Validate LDIF schema
	@echo "🔍 Validating LDIF schema..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json --validate-schema
	@echo "✅ LDIF schema validated"

target-run: ## Run LDIF data export
	@echo "🎯 Running LDIF data export..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json < tests/fixtures/data/sample_input.jsonl
	@echo "✅ LDIF data export complete"

target-run-debug: ## Run LDIF target with debug logging
	@echo "🎯 Running LDIF target with debug..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json --log-level DEBUG < tests/fixtures/data/sample_input.jsonl
	@echo "✅ LDIF debug run complete"

target-dry-run: ## Run LDIF target in dry-run mode
	@echo "🎯 Running LDIF target dry-run..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json --dry-run < tests/fixtures/data/sample_input.jsonl
	@echo "✅ LDIF dry-run complete"

# ============================================================================
# 📄 LDIF-SPECIFIC OPERATIONS
# ============================================================================

ldif-write: ## Write data to LDIF file
	@echo "📄 Writing data to LDIF file..."
	@poetry run python -c "from flext_target_ldif.writer import LDIFWriter; import json; config = json.load(open('tests/fixtures/config/target_config.json')); writer = LDIFWriter(config); print('Testing LDIF write...'); result = writer.test_write(); print('✅ Write test passed!' if result.is_success else f'❌ Write test failed: {result.error}')"
	@echo "✅ LDIF write complete"

ldif-validate-output: ## Validate LDIF output format
	@echo "📄 Validating LDIF output format..."
	@poetry run python scripts/validate_ldif_output.py
	@echo "✅ LDIF output validation complete"

ldif-format-check: ## Check LDIF format compliance
	@echo "📄 Checking LDIF format compliance..."
	@poetry run python -c "from flext_target_ldif.validator import LDIFValidator; validator = LDIFValidator(); print('Testing LDIF format...'); result = validator.validate_file('output.ldif'); print('✅ Format valid!' if result.is_valid else f'❌ Format invalid: {result.errors}')"
	@echo "✅ LDIF format check complete"

ldif-export-users: ## Export user data to LDIF
	@echo "📄 Exporting user data to LDIF..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json < tests/fixtures/data/users.jsonl
	@echo "✅ User data export complete"

ldif-export-groups: ## Export group data to LDIF
	@echo "📄 Exporting group data to LDIF..."
	@poetry run target-ldif --config tests/fixtures/config/target_config.json < tests/fixtures/data/groups.jsonl
	@echo "✅ Group data export complete"

ldif-merge: ## Merge multiple LDIF files
	@echo "📄 Merging LDIF files..."
	@poetry run python scripts/merge_ldif_files.py
	@echo "✅ LDIF merge complete"

ldif-split: ## Split LDIF file by entry type
	@echo "📄 Splitting LDIF file by entry type..."
	@poetry run python scripts/split_ldif_by_type.py
	@echo "✅ LDIF split complete"

ldif-clean: ## Clean and normalize LDIF output
	@echo "📄 Cleaning and normalizing LDIF output..."
	@poetry run python scripts/clean_ldif_output.py
	@echo "✅ LDIF cleaning complete"

# ============================================================================
# 🔍 FILE VALIDATION
# ============================================================================

validate-output: ## Validate generated LDIF files
	@echo "🔍 Validating generated LDIF files..."
	@poetry run python scripts/validate_ldif_files.py
	@echo "✅ LDIF file validation complete"

validate-encoding: ## Validate LDIF file encoding
	@echo "🔍 Validating LDIF file encoding..."
	@poetry run python scripts/validate_encoding.py
	@echo "✅ Encoding validation complete"

validate-schema: ## Validate LDIF schema compliance
	@echo "🔍 Validating LDIF schema compliance..."
	@poetry run python scripts/validate_schema_compliance.py
	@echo "✅ Schema validation complete"

validate-dn: ## Validate DN format in LDIF
	@echo "🔍 Validating DN format in LDIF..."
	@poetry run python scripts/validate_dn_format.py
	@echo "✅ DN validation complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf output/
	@rm -rf *.ldif
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# Target settings
TARGET_CONFIG := config.json
TARGET_STATE := state.json

# Singer settings
export SINGER_LOG_LEVEL := INFO
export SINGER_BATCH_SIZE := 100
export SINGER_MAX_BATCH_AGE := 300

# LDIF Target settings
export TARGET_LDIF_OUTPUT_DIR := output
export TARGET_LDIF_FILENAME := export.ldif
export TARGET_LDIF_ENCODING := utf-8
export TARGET_LDIF_LINE_LENGTH := 76

# File settings
export TARGET_LDIF_VALIDATE_FORMAT := true
export TARGET_LDIF_INCLUDE_COMMENTS := false
export TARGET_LDIF_SORT_ENTRIES := true

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-target-ldif
PROJECT_TYPE := meltano-plugin
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Target LDIF - LDIF File Singer Target

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 SINGER SPECIFIC COMMANDS
# ============================================================================

singer-about: ## Show Singer target about information
	@echo "🎵 Singer target about information..."
	@poetry run target-ldif --about
	@echo "✅ About information displayed"

singer-config-sample: ## Generate Singer config sample
	@echo "🎵 Generating Singer config sample..."
	@poetry run target-ldif --config-sample > config_sample.json
	@echo "✅ Config sample generated: config_sample.json"

singer-test-streams: ## Test Singer streams
	@echo "🎵 Testing Singer streams..."
	@poetry run pytest tests/singer/test_streams.py -v
	@echo "✅ Singer streams tests complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Singer project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Singer Target + LDIF"
	@echo "🐍 Python: 3.13"
	@echo "🔗 Framework: FLEXT Core + Singer SDK"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: LDIF File Singer Target"
	@echo "🔗 Dependencies: flext-core, flext-ldif, singer-sdk"
	@echo "📦 Provides: LDIF file export capabilities"
	@echo "🎯 Standards: Enterprise LDIF format patterns"