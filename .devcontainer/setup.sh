#!/bin/bash

set -e

echo "🚀 Setting up Dagster + dbt + Snowflake Demo environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install additional system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    build-essential \
    curl \
    git \
    unzip \
    vim \
    tree

# Navigate to workspace
cd /workspaces/dagster-snowflake-dbt-demo

# Create and activate virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install wheel
echo "📦 Upgrading pip and installing wheel..."
pip install --upgrade pip setuptools wheel

# Install Python dependencies for dagster-demo
echo "📋 Installing Dagster dependencies..."
cd dagster-demo
pip install -e ".[dev]"

# Install dbt dependencies
echo "📋 Installing dbt dependencies..."
cd ..
pip install dbt-core dbt-duckdb dbt-snowflake

# Install additional development tools
echo "🛠️ Installing development tools..."
pip install \
    black \
    ruff \
    isort \
    pytest \
    pre-commit

# Install uv for faster package management (optional)
echo "🚀 Installing uv for faster package management..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Dagger CLI
echo "🔥 Installing Dagger CLI..."
curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=/usr/local/bin sudo -E sh

# Make scripts executable
echo "🔑 Making scripts executable..."
chmod +x scripts/*.sh

# Set up git configuration
echo "🔧 Setting up git configuration..."
git config --global init.defaultBranch main
git config --global pull.rebase false

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p ~/.dagster
mkdir -p ~/.dbt

# Create dbt profiles directory and basic configuration
echo "📊 Setting up dbt profiles..."
mkdir -p ~/.dbt
cat > ~/.dbt/profiles.yml << 'EOF'
dbt_demo:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: /tmp/dbt_demo.duckdb
      
    # Snowflake configuration (requires environment variables)
    snowflake:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE', 'ACCOUNTADMIN') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE', 'DEMO_DB') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH') }}"
      schema: "{{ env_var('SNOWFLAKE_SCHEMA', 'PUBLIC') }}"
      threads: 4
      keepalives_idle: 0
      search_path: "{{ env_var('SNOWFLAKE_SCHEMA', 'PUBLIC') }}"
EOF

# Set up environment variables template
echo "🔐 Creating environment variables template..."
cat > .env.template << 'EOF'
# Snowflake Configuration
# Copy this file to .env and fill in your actual values
SNOWFLAKE_ACCOUNT=your-account.snowflakecomputing.com
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_DATABASE=DEMO_DB
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_SCHEMA=PUBLIC

# Dagster Configuration
DAGSTER_HOME=/workspaces/dagster-snowflake-dbt-demo/.dagster
EOF

# Add .env to .gitignore if not already there
if ! grep -q ".env" .gitignore 2>/dev/null; then
    echo ".env" >> .gitignore
fi

# Create activation script for easy venv activation
echo "📝 Creating virtual environment activation helper..."
cat > activate.sh << 'EOF'
#!/bin/bash
# Quick script to activate the virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated!"
echo "Python: $(which python)"
echo "pip: $(which pip)"
EOF
chmod +x activate.sh

# Add venv activation to .bashrc for automatic activation
echo "🔧 Setting up automatic venv activation..."
echo "" >> ~/.bashrc
echo "# Auto-activate virtual environment in Codespaces" >> ~/.bashrc
echo "if [ -f /workspaces/dagster-snowflake-dbt-demo/venv/bin/activate ]; then" >> ~/.bashrc
echo "    source /workspaces/dagster-snowflake-dbt-demo/venv/bin/activate" >> ~/.bashrc
echo "fi" >> ~/.bashrc

# Create a simple test to verify setup
echo "✅ Creating setup verification test..."
cat > verify_setup.py << 'EOF'
#!/usr/bin/env python3

import sys
import subprocess
import os

def run_command(cmd, description):
    print(f"Testing {description}...")
    try:
        # Ensure we're using the venv
        env = os.environ.copy()
        if 'VIRTUAL_ENV' in env:
            venv_path = env['VIRTUAL_ENV']
            env['PATH'] = f"{venv_path}/bin:{env['PATH']}"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env=env)
        if result.returncode == 0:
            print(f"  ✅ {description} - OK")
            if description == "Python installation":
                print(f"     Version: {result.stdout.strip()}")
            return True
        else:
            print(f"  ❌ {description} - FAILED")
            print(f"     Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏱️ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"  💥 {description} - EXCEPTION: {e}")
        return False

def main():
    print("🧪 Verifying Codespace setup...\n")
    
    # Check if we're in a virtual environment
    if 'VIRTUAL_ENV' in os.environ:
        print(f"✅ Virtual environment active: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️ Virtual environment not detected")
    
    tests = [
        ("python --version", "Python installation"),
        ("pip --version", "pip installation"),
        ("dagger version", "Dagger CLI"),
        ("dbt --version", "dbt installation"),
        ("python -c 'import dagster; print(f\"Dagster {dagster.__version__}\")'", "Dagster import"),
        ("ls /workspaces/dagster-snowflake-dbt-demo/scripts/run-ci.sh", "CI scripts"),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, desc in tests:
        if run_command(cmd, desc):
            passed += 1
    
    print(f"\n📊 Setup verification: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Codespace is ready to go!")
        print("\n📚 Quick start commands:")
        print("  source venv/bin/activate          - Activate virtual environment")
        print("  ./activate.sh                     - Quick activation script")
        print("  ./scripts/run-step.sh help        - Show all available commands")
        print("  ./scripts/run-step.sh validate-dbt - Test dbt configuration")
        print("  ./scripts/run-ci.sh               - Run full CI pipeline")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

# Run the verification test (within venv)
echo "🧪 Running setup verification..."
python verify_setup.py

echo ""
echo "🎉 Codespace setup complete!"
echo ""
echo "📚 Next steps:"
echo "  1. Virtual environment is created and activated automatically"
echo "  2. Copy .env.template to .env and fill in your Snowflake credentials"
echo "  3. Run './scripts/run-step.sh help' to see available commands"
echo "  4. Run './scripts/run-step.sh validate-dbt' to test your setup"
echo "  5. Run './scripts/run-ci.sh' to execute the full CI pipeline"
echo ""
echo "🔗 Useful commands:"
echo "  source venv/bin/activate  - Manually activate venv (auto-activated in new terminals)"
echo "  ./activate.sh             - Quick activation script"
echo "  deactivate                - Deactivate virtual environment"
echo ""
echo "🔗 Useful ports:"
echo "  - Port 3000: Dagster Web UI"
echo "  - Port 8080: dbt Documentation"
echo ""
