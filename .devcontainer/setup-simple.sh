#!/bin/bash

set -e

echo "🚀 Setting up simplified Dagster + dbt + Snowflake Demo environment..."

# Navigate to workspace
cd /workspaces/dagster-snowflake-dbt-demo

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install basic Python dependencies
echo "📋 Installing basic dependencies..."
pip install dagster dbt-core dbt-snowflake

echo "✅ Simple setup complete!"
echo "Next steps:"
echo "  1. source venv/bin/activate"
echo "  2. Install additional packages as needed"
echo "  3. Configure your Snowflake credentials"
