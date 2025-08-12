#!/bin/bash

set -e

echo "🚀 Setting up Dagster + dbt + Snowflake Demo environment..."

# Navigate to workspace
cd /workspaces/dagster-snowflake-dbt-demo

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install uv for faster package management
echo "🚀 Installing uv for faster package management..."
pip install uv

# Install dagster-demo package with all dependencies using uv
echo "📋 Installing Dagster demo package with all dependencies..."
cd dagster-demo
uv pip install -e ".[dev]"
cd ..

# Install dbt dependencies
echo "📋 Installing dbt dependencies..."
uv pip install dbt-core dbt-snowflake

echo "✅ Setup complete!"
echo "🎉 Ready to run 'dagster dev' in the dagster-demo folder!"
echo ""
echo "Next steps:"
echo "  1. source venv/bin/activate"
echo "  2. cd dagster-demo && dagster dev"
echo "  3. Configure your Snowflake credentials"
