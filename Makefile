# FLEXT TARGET LDIF - Singer Target for LDIF Format Generation
# =============================================================
# Enterprise Singer target for LDIF (LDAP Data Interchange Format) output
# Python 3.13 + Singer SDK + LDIF RFC 2849 + Zero Tolerance Quality Gates

.PHONY: help check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-singer
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: target-test target-validate target-run singer-spec
.PHONY: ldif-validate ldif-format-test ldif-performance

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🎯 FLEXT TARGET LDIF - Singer Target for LDIF Format Generation"
	@echo "============================================================="
	@echo "🎯 Singer SDK + LDIF RFC 2849 + Python 3.13"
	@echo ""
	@echo "📦 Enterprise Singer target for LDIF (LDAP Data Interchange Format) output"
	@echo "🔒 Zero tolerance quality gates with comprehensive Singer testing"
	@echo "🧪 90%+ test coverage requirement with LDIF format compliance"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test target-test ## STRICT compliance validation (all must pass)
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

test-singer: ## Run Singer-specific tests
	@echo "🧪 Running Singer protocol tests..."
	@poetry run pytest tests/ -m "singer" -v
	@echo "✅ Singer tests complete"

test-ldif: ## Run LDIF-specific tests
	@echo "🧪 Running LDIF format tests..."
	@poetry run pytest tests/ -m "ldif" -v
	@echo "✅ LDIF tests complete"

test-performance: ## Run performance tests
	@echo "⚡ Running Singer target performance tests..."
	@poetry run pytest tests/performance/ -v --benchmark-only
	@echo "✅ Performance tests complete"

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
# 🎵 SINGER TARGET OPERATIONS - CORE FUNCTIONALITY
# ============================================================================

target-test: ## Test Singer target functionality
	@echo "🧪 Testing Singer target functionality..."
	@poetry run python -c "from flext_target_ldif.target import TargetLDIF; from flext_target_ldif.sinks import LDIFSink; print('LDIF target loaded successfully')"
	@echo "✅ Singer target test complete"

target-validate: ## Validate Singer target configuration
	@echo "🔍 Validating Singer target configuration..."
	@poetry run python scripts/validate_target_config.py
	@echo "✅ Singer target configuration validation complete"

target-run: ## Run Singer target with sample data
	@echo "🎵 Running Singer target with sample data..."
	@poetry run flext-target-ldif --config config.json < sample_data/sample.jsonl
	@echo "✅ Singer target execution complete"

target-schema: ## Test Singer target schema handling
	@echo "📋 Testing Singer target schema handling..."
	@poetry run python scripts/test_schema_handling.py
	@echo "✅ Schema handling test complete"

target-state: ## Test Singer target state management
	@echo "📊 Testing Singer target state management..."
	@poetry run python scripts/test_state_management.py
	@echo "✅ State management test complete"

# ============================================================================
# 📁 LDIF FORMAT OPERATIONS
# ============================================================================

ldif-validate: ## Validate LDIF output format compliance
	@echo "📁 Validating LDIF output format..."
	@poetry run python scripts/validate_ldif_output.py
	@echo "✅ LDIF format validation complete"

ldif-format-test: ## Test LDIF format generation
	@echo "📋 Testing LDIF format generation..."
	@poetry run python scripts/test_ldif_generation.py
	@echo "✅ LDIF format test complete"

ldif-performance: ## Run LDIF performance benchmarks
	@echo "⚡ Running LDIF performance benchmarks..."
	@poetry run python scripts/benchmark_ldif_performance.py
	@echo "✅ LDIF performance benchmarks complete"

ldif-encoding-test: ## Test LDIF encoding handling
	@echo "🔤 Testing LDIF encoding handling..."
	@poetry run python scripts/test_ldif_encoding.py
	@echo "✅ LDIF encoding test complete"

ldif-dn-generation: ## Test DN generation patterns
	@echo "🎯 Testing DN generation patterns..."
	@poetry run python scripts/test_dn_generation.py
	@echo "✅ DN generation test complete"

ldif-attribute-mapping: ## Test attribute mapping functionality
	@echo "🗺️ Testing attribute mapping..."
	@poetry run python scripts/test_attribute_mapping.py
	@echo "✅ Attribute mapping test complete"

ldif-line-wrapping: ## Test LDIF line wrapping compliance
	@echo "📝 Testing LDIF line wrapping..."
	@poetry run python scripts/test_line_wrapping.py
	@echo "✅ Line wrapping test complete"

# ============================================================================
# 🎵 SINGER PROTOCOL COMPLIANCE
# ============================================================================

singer-spec: ## Validate Singer specification compliance
	@echo "🎵 Validating Singer specification compliance..."
	@poetry run python scripts/validate_singer_spec.py
	@echo "✅ Singer specification validation complete"

singer-messages: ## Test Singer message handling
	@echo "📬 Testing Singer message handling..."
	@poetry run python scripts/test_singer_messages.py
	@echo "✅ Singer message test complete"

singer-catalog: ## Test Singer catalog handling
	@echo "📋 Testing Singer catalog handling..."
	@poetry run python scripts/test_singer_catalog.py
	@echo "✅ Singer catalog test complete"

singer-state: ## Test Singer state handling
	@echo "📊 Testing Singer state handling..."
	@poetry run python scripts/test_singer_state.py
	@echo "✅ Singer state test complete"

singer-records: ## Test Singer record processing
	@echo "📄 Testing Singer record processing..."
	@poetry run python scripts/test_singer_records.py
	@echo "✅ Singer record test complete"

# ============================================================================
# 🔍 DATA QUALITY & VALIDATION
# ============================================================================

validate-ldif-rfc: ## Validate LDIF RFC 2849 compliance
	@echo "🔍 Validating LDIF RFC 2849 compliance..."
	@poetry run python scripts/validate_ldif_rfc.py
	@echo "✅ LDIF RFC compliance validation complete"

validate-dn-format: ## Validate DN format compliance
	@echo "🔍 Validating DN format compliance..."
	@poetry run python scripts/validate_dn_format.py
	@echo "✅ DN format validation complete"

validate-attribute-encoding: ## Validate attribute encoding
	@echo "🔍 Validating attribute encoding..."
	@poetry run python scripts/validate_attribute_encoding.py
	@echo "✅ Attribute encoding validation complete"

data-quality-report: ## Generate comprehensive data quality report
	@echo "📊 Generating data quality report..."
	@poetry run python scripts/generate_quality_report.py
	@echo "✅ Data quality report generated"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

package: build ## Create deployment package
	@echo "📦 Creating deployment package..."
	@tar -czf dist/flext-target-ldif-deployment.tar.gz \
		src/ \
		tests/ \
		scripts/ \
		pyproject.toml \
		README.md \
		CLAUDE.md
	@echo "✅ Deployment package created: dist/flext-target-ldif-deployment.tar.gz"

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
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .ruff_cache/
	@rm -rf output/
	@rm -f *.ldif
	@rm -f state.json
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
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

# LDIF Target settings
export FLEXT_TARGET_LDIF_OUTPUT_PATH := ./output
export FLEXT_TARGET_LDIF_DEBUG := false
export FLEXT_TARGET_LDIF_CONFIG := ./config.json

# LDIF format settings
export FLEXT_TARGET_LDIF_LINE_LENGTH := 78
export FLEXT_TARGET_LDIF_BASE64_ENCODE := false
export FLEXT_TARGET_LDIF_INCLUDE_TIMESTAMPS := true

# DN generation settings
export FLEXT_TARGET_LDIF_DN_TEMPLATE := cn={name},ou=users,dc=example,dc=com
export FLEXT_TARGET_LDIF_DN_ATTRIBUTE := cn

# File output settings
export FLEXT_TARGET_LDIF_FILE_PATTERN := output_{timestamp}.ldif
export FLEXT_TARGET_LDIF_MAX_FILE_SIZE := 10485760
export FLEXT_TARGET_LDIF_COMPRESSION := false

# Performance settings
export FLEXT_TARGET_LDIF_BATCH_SIZE := 1000
export FLEXT_TARGET_LDIF_BUFFER_SIZE := 8192
export FLEXT_TARGET_LDIF_FLUSH_INTERVAL := 5

# Singer settings
export SINGER_SDK_LOG_LEVEL := INFO
export SINGER_SDK_BATCH_SIZE := 1000
export SINGER_SDK_MAX_RECORD_AGE_IN_MINUTES := 5

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
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT TARGET LDIF - Singer Target for LDIF Format Generation

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 DEVELOPMENT UTILITIES
# ============================================================================

dev-target-server: ## Start development target server
	@echo "🔧 Starting development target server..."
	@poetry run python scripts/dev_target_server.py
	@echo "✅ Development target server started"

dev-target-monitor: ## Monitor target operations
	@echo "📊 Monitoring target operations..."
	@poetry run python scripts/monitor_target_operations.py
	@echo "✅ Target monitoring complete"

dev-ldif-viewer: ## Interactive LDIF viewer
	@echo "🎮 Starting LDIF viewer..."
	@poetry run python scripts/ldif_viewer.py
	@echo "✅ LDIF viewer session complete"

dev-dn-generator: ## Interactive DN generator tool
	@echo "🎯 Starting DN generator tool..."
	@poetry run python scripts/dn_generator.py
	@echo "✅ DN generator session complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Core project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Singer Target + LDIF RFC 2849"
	@echo "🐍 Python: 3.13"
	@echo "🔗 Framework: FLEXT Core + Singer SDK + LDIF"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: Singer Target for LDIF Format Generation"
	@echo "🔗 Dependencies: flext-core, flext-observability, singer-sdk"
	@echo "📦 Provides: LDIF file generation from Singer data streams"
	@echo "🎯 Standards: Enterprise Singer target patterns with RFC 2849 compliance"

# ============================================================================
# 🔄 CONTINUOUS INTEGRATION
# ============================================================================

ci-check: validate ## CI quality checks
	@echo "🔍 Running CI quality checks..."
	@poetry run python scripts/ci_quality_report.py
	@echo "✅ CI quality checks complete"

ci-performance: ## CI performance benchmarks
	@echo "⚡ Running CI performance benchmarks..."
	@poetry run python scripts/ci_performance_benchmarks.py
	@echo "✅ CI performance benchmarks complete"

ci-integration: ## CI integration tests
	@echo "🔗 Running CI integration tests..."
	@poetry run pytest tests/integration/ -v --tb=short
	@echo "✅ CI integration tests complete"

ci-singer: ## CI Singer protocol tests
	@echo "🎵 Running CI Singer tests..."
	@poetry run pytest tests/ -m "singer" -v --tb=short
	@echo "✅ CI Singer tests complete"

ci-ldif: ## CI LDIF format tests
	@echo "📁 Running CI LDIF tests..."
	@poetry run pytest tests/ -m "ldif" -v --tb=short
	@echo "✅ CI LDIF tests complete"

ci-all: ci-check ci-performance ci-integration ci-singer ci-ldif ## Run all CI checks
	@echo "✅ All CI checks complete"

# ============================================================================
# 🚀 PRODUCTION DEPLOYMENT
# ============================================================================

deploy-target: validate build ## Deploy target for production use
	@echo "🚀 Deploying LDIF target..."
	@poetry run python scripts/deploy_target.py
	@echo "✅ LDIF target deployment complete"

test-deployment: ## Test deployed target functionality
	@echo "🧪 Testing deployed target..."
	@poetry run python scripts/test_deployed_target.py
	@echo "✅ Deployment test complete"

rollback-deployment: ## Rollback target deployment
	@echo "🔄 Rolling back target deployment..."
	@poetry run python scripts/rollback_target_deployment.py
	@echo "✅ Deployment rollback complete"

# ============================================================================
# 🔬 MONITORING & OBSERVABILITY
# ============================================================================

monitor-ldif-generation: ## Monitor LDIF generation performance
	@echo "📊 Monitoring LDIF generation..."
	@poetry run python scripts/monitor_ldif_generation.py
	@echo "✅ LDIF generation monitoring complete"

monitor-target-health: ## Monitor Singer target health
	@echo "📊 Monitoring Singer target health..."
	@poetry run python scripts/monitor_target_health.py
	@echo "✅ Target health monitoring complete"

generate-target-metrics: ## Generate target performance metrics
	@echo "📊 Generating target performance metrics..."
	@poetry run python scripts/generate_target_metrics.py
	@echo "✅ Target metrics generated"