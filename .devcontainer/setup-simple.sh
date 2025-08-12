#!/bin/bash

set -e

echo "🚀 Setting up Dagster + dbt + Snowflake Demo environment..."

# Navigate to workspace
cd /workspaces/dagster-snowflake-dbt-demo

# Create and activate virtual environment with proper symlinks
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv --copies
source venv/bin/activate

# Verify virtual environment
echo "Python location: $(which python)"
echo "Python version: $(python --version)"

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

# Install additional dependencies required by dagster-demo
echo "📋 Installing additional Python packages..."
uv pip install pandas matplotlib seaborn plotly

# Install dbt dependencies
echo "📋 Installing dbt dependencies..."
uv pip install dbt-core dbt-snowflake

# Parse dbt project to generate manifest
echo "📋 Parsing dbt project..."
cd dbt_demo
dbt parse
cd ..

echo "✅ Setup complete!"
echo "🎉 Ready to run 'dagster dev' in the dagster-demo folder!"
echo ""
echo "Next steps:"
echo "  1. source venv/bin/activate"
echo "  2. cd dagster-demo && dagster dev"
echo "  3. Alternative: Use 'python -m dagster dev' if direct 'dagster' command fails"
echo "  4. Configure your Snowflake credentials"
