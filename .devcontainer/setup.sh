#!/bin/bash

set -e

echo "🚀 Setting up Dagster Snowflake dbt development environment..."

# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install system dependencies
sudo apt-get install -y \
    build-essential \
    curl \
    git \
    unzip \
    vim \
    jq \
    tree

# Upgrade pip and install Python package managers
python -m pip install --upgrade pip
pip install poetry

# Install core Python packages for data engineering
pip install \
    dagster \
    dagster-webserver \
    dagster-postgres \
    dagster-docker \
    dagster-snowflake \
    dbt-core \
    dbt-snowflake \
    snowflake-connector-python \
    pandas \
    numpy \
    sqlalchemy \
    psycopg2-binary \
    jupyter \
    jupyterlab \
    plotly \
    streamlit \
    great-expectations \
    pytest \
    pytest-cov \
    black \
    isort \
    flake8 \
    mypy

# Install dbt packages
dbt --version

# Create necessary directories
mkdir -p /opt/dagster/dagster_home
mkdir -p .dbt
mkdir -p logs
mkdir -p data
mkdir -p tests

# Set up Dagster home
export DAGSTER_HOME=/opt/dagster/dagster_home

# Create a basic dagster.yaml if it doesn't exist
if [ ! -f /opt/dagster/dagster_home/dagster.yaml ]; then
    cat > /opt/dagster/dagster_home/dagster.yaml << EOF
storage:
  postgres:
    postgres_url: postgresql://dagster:dagster@localhost:5432/dagster

compute_logs:
  module: dagster.core.storage.local_compute_log_manager
  class: LocalComputeLogManager
  config:
    base_dir: /opt/dagster/dagster_home/logs

local_artifact_storage:
  module: dagster.core.storage.file_manager
  class: LocalFileManager
  config:
    base_dir: /opt/dagster/dagster_home/storage
EOF
fi

# Create basic project structure if files don't exist
if [ ! -f requirements.txt ]; then
    cat > requirements.txt << EOF
dagster
dagster-webserver
dagster-snowflake
dbt-core
dbt-snowflake
snowflake-connector-python
pandas
numpy
great-expectations
streamlit
EOF
fi

if [ ! -f pyproject.toml ]; then
    cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools", "wheel"]

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
EOF
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Dagster
.dagster/
dagster_home/
logs/
storage/

# dbt
dbt_packages/
target/
profiles.yml
.dbt/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/settings.json
.idea/

# OS
.DS_Store
Thumbs.db

# Data files
*.csv
*.parquet
*.json
data/

# Jupyter
.ipynb_checkpoints/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Snowflake
*.p8
EOF
fi

# Set proper permissions
sudo chown -R vscode:vscode /opt/dagster/dagster_home
sudo chmod -R 755 /opt/dagster/dagster_home

echo "✅ Development environment setup complete!"
echo "🎯 Next steps:"
echo "   1. Add your Snowflake credentials to .env file"
echo "   2. Configure dbt profiles in .dbt/profiles.yml"
echo "   3. Start building your Dagster assets and dbt models!"
echo ""
echo "🚀 Useful commands:"
echo "   - dagster dev (start Dagster web server)"
echo "   - dbt run (run dbt models)"
echo "   - jupyter lab (start Jupyter lab)"
echo "   - streamlit run app.py (run Streamlit app)"
