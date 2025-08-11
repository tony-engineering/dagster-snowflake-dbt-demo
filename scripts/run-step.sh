#!/bin/bash

# Run individual CI steps using Dagger
set -e

STEP="${1:-help}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case $STEP in
    "lint")
        echo "🔍 Running code linting..."
        dagger -m "$PROJECT_ROOT/.dagger" call lint-code --source="$PROJECT_ROOT"
        ;;
    "test")
        echo "🧪 Running Dagster tests..."
        dagger -m "$PROJECT_ROOT/.dagger" call test-dagster --source="$PROJECT_ROOT"
        ;;
    "validate-dagster")
        echo "✅ Validating Dagster definitions..."
        dagger -m "$PROJECT_ROOT/.dagger" call validate-dagster-definitions --source="$PROJECT_ROOT"
        ;;
    "validate-dbt")
        echo "🔧 Validating dbt models..."
        dagger -m "$PROJECT_ROOT/.dagger" call validate-dbt --source="$PROJECT_ROOT"
        ;;
    "security")
        echo "🔒 Running security scan..."
        dagger -m "$PROJECT_ROOT/.dagger" call security-scan --source="$PROJECT_ROOT"
        ;;
    "docs")
        echo "📚 Building documentation..."
        dagger -m "$PROJECT_ROOT/.dagger" call build-documentation --source="$PROJECT_ROOT"
        ;;
    "ci")
        echo "🚀 Running full CI pipeline..."
        dagger -m "$PROJECT_ROOT/.dagger" call full-ci-pipeline --source="$PROJECT_ROOT"
        ;;
    "help"|*)
        echo "Usage: $0 [STEP]"
        echo ""
        echo "Available steps:"
        echo "  lint              - Run code linting (ruff, black, isort)"
        echo "  test              - Run Dagster tests"
        echo "  validate-dagster  - Validate Dagster definitions"
        echo "  validate-dbt      - Validate dbt models and config"
        echo "  security          - Run security scan"
        echo "  docs              - Build documentation"
        echo "  ci                - Run full CI pipeline"
        echo ""
        echo "Example: $0 lint"
        ;;
esac
