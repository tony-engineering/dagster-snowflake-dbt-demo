#!/bin/bash

# Run CI pipeline locally using Dagger
set -e

echo "🚀 Running Dagster + dbt CI pipeline with Dagger..."

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Run the full CI pipeline
dagger -m "$PROJECT_ROOT/.dagger" call full-ci-pipeline --source="$PROJECT_ROOT"

echo "✅ CI pipeline completed!"
