# GitHub Codespaces Setup

Complete GitHub Codespaces configuration for the Dagster + dbt + Snowflake Demo project.

## 🚀 Quick Start

1. **Open in Codespaces**: Click "Code" → "Codespaces" → "Create codespace on main"

2. **Wait for Setup**: The setup script runs automatically (~3-5 minutes)

3. **Configure Snowflake** (Optional):
   ```bash
   cp .env.template .env
   # Edit .env with your Snowflake credentials
   ```

4. **Test Your Setup**:
   ```bash
   ./scripts/run-step.sh help              # Show available commands
   ./scripts/run-step.sh validate-dbt      # Test dbt configuration
   ./scripts/run-ci.sh                     # Run full CI pipeline
   ```

## 📦 What's Included

### Development Environment
- **Python 3.13**: Latest Python version with virtual environment
- **Docker**: Docker-in-Docker for Dagger CI/CD
- **GitHub CLI**: Integrated GitHub tooling
- **VS Code Extensions**: Dagster, dbt, Python, SQL, and more

### Data Stack Tools
- **Dagster**: Data orchestration and asset management
- **dbt**: Data transformation with SQL
- **DuckDB**: Local development database
- **Snowflake**: Cloud data warehouse support
- **Dagger**: Modern CI/CD pipeline

### Development Tools
- **Code Quality**: Black, Ruff, isort for Python formatting/linting
- **Testing**: pytest for unit and integration tests
- **Security**: Dependency vulnerability scanning
- **Documentation**: Auto-generated docs for dbt and Dagster

## 🐍 Virtual Environment

The setup automatically creates and manages a Python virtual environment:

- **Location**: `venv/` directory in project root
- **Auto-activation**: New terminals automatically activate the venv
- **Manual commands**:
  ```bash
  source venv/bin/activate    # Manual activation
  ./activate.sh              # Quick activation script  
  deactivate                 # Deactivate environment
  ```

## 🔧 Configuration Files

### `.devcontainer/devcontainer.json`
- **Base Image**: Python 3.13 on Debian Bullseye
- **Features**: Docker-in-Docker, GitHub CLI
- **VS Code Extensions**: Python, Dagster, dbt, SQL support
- **Port Forwarding**: 3000 (Dagster UI), 8080 (dbt docs)
- **Environment**: Virtual environment pre-configured

### `.devcontainer/setup.sh`
- Creates Python virtual environment
- Installs all project dependencies
- Configures dbt profiles for DuckDB and Snowflake
- Sets up development tools
- Installs Dagger CLI
- Runs verification tests

## 🌐 Port Forwarding

The following ports are automatically forwarded:

| Port | Service | Command to Start |
|------|---------|------------------|
| 3000 | Dagster Web UI | `dagster dev -f dagster_demo/definitions.py` |
| 8080 | dbt Documentation | `cd dbt_demo && dbt docs generate && dbt docs serve --port 8080` |

## 🔐 Environment Variables

Copy `.env.template` to `.env` and configure:

```env
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your-account.snowflakecomputing.com
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_DATABASE=DEMO_DB
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_SCHEMA=PUBLIC

# Dagster Configuration  
DAGSTER_HOME=/workspaces/dagster-snowflake-dbt-demo/.dagster
```

## 📚 Common Commands

### Virtual Environment
```bash
source venv/bin/activate        # Activate (auto-activated in new terminals)
./activate.sh                   # Quick activation script
deactivate                      # Deactivate
```

### CI/CD Pipeline
```bash
./scripts/run-step.sh help      # Show all available commands
./scripts/run-step.sh lint      # Code quality checks  
./scripts/run-step.sh test      # Run Dagster tests
./scripts/run-step.sh validate-dagster  # Validate Dagster definitions
./scripts/run-step.sh validate-dbt      # Validate dbt models
./scripts/run-step.sh security  # Security vulnerability scan
./scripts/run-ci.sh            # Full CI pipeline
```

### Dagster Development
```bash
cd dagster-demo

# Start Dagster web UI (accessible on port 3000)
dagster dev -f dagster_demo/definitions.py

# Run specific assets
dagster asset materialize --select my_asset_name

# View asset lineage and execution history in web UI
```

### dbt Development  
```bash
cd dbt_demo

# Test configuration
dbt debug

# Run models with DuckDB (local development)
dbt run --target dev

# Run models with Snowflake (requires .env configuration)
dbt run --target snowflake

# Generate and serve documentation
dbt docs generate
dbt docs serve --port 8080

# Run tests
dbt test
```

## 🛠️ VS Code Extensions

The following extensions are automatically installed:

| Extension | Purpose |
|-----------|---------|
| Python | Core Python development support |
| Pylance | Python language server |
| Black Formatter | Code formatting |
| Ruff | Fast Python linting |
| isort | Import sorting |
| dbt Power User | Enhanced dbt development |
| Dagster | Dagster-specific tooling |
| SQL | SQL syntax highlighting |
| Docker | Container management |
| GitHub Actions | Workflow editing |

## 🔍 Troubleshooting

### Setup Issues
```bash
# Re-run setup script
bash .devcontainer/setup.sh

# Verify setup
python verify_setup.py

# Check virtual environment
which python
echo $VIRTUAL_ENV
```

### Virtual Environment Issues
```bash
# Recreate if corrupted
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Reinstall dependencies
cd dagster-demo
pip install -e ".[dev]"
cd ../
pip install dbt-core dbt-duckdb dbt-snowflake
```

### Port Access Issues
- Check "Ports" tab in VS Code terminal panel
- Ensure services are running on correct ports
- Use Command Palette → "Forward a Port" for manual forwarding

### Snowflake Connection Issues
1. Verify `.env` file exists with correct credentials
2. Test connection: `cd dbt_demo && dbt debug --target snowflake`  
3. Check Snowflake account permissions and network access
4. Verify account URL format: `account-name.region.snowflakecomputing.com`

### Performance Issues
- Stop unused services to conserve resources
- Use DuckDB for local development (faster than Snowflake)
- Clear `.dagster` cache if disk space is low

## 🏗️ File Structure

```
dagster-snowflake-dbt-demo/
├── .devcontainer/
│   ├── devcontainer.json       # Codespaces configuration
│   └── setup.sh               # Environment setup script
├── dagster-demo/              # Dagster orchestration code
├── dbt_demo/                  # dbt transformation models  
├── scripts/                   # CI/CD pipeline scripts
├── venv/                      # Python virtual environment (created)
├── .env.template              # Environment variables template
├── activate.sh               # Quick venv activation (created)
├── verify_setup.py           # Setup verification (created)
└── GH_CODESPACES.md          # This documentation
```

## ⚡ Performance Tips

### Local Development
- Use DuckDB target for faster iteration: `dbt run --target dev`
- Keep Dagster UI running for asset lineage visualization
- Use `./scripts/run-step.sh` for focused testing

### Resource Management
- **Persistent Storage**: `.dagster` directory persists across sessions
- **Volume Mounts**: Dagster cache is stored in Docker volume
- **Parallel Execution**: Dagger runs pipeline steps in parallel
- **Efficient Uploads**: `.daggerignore` excludes unnecessary files

### CI/CD Optimization
- Individual steps: `./scripts/run-step.sh <step-name>`
- Full pipeline: `./scripts/run-ci.sh`
- Local testing before push to avoid CI failures

## 📖 Additional Resources

- **Main Project**: See [README.md](./README.md) for project overview
- **Quick Start**: See [QUICK_START.md](./QUICK_START.md) for Dagger CI/CD details
- **Dagster Docs**: [docs.dagster.io](https://docs.dagster.io)
- **dbt Docs**: [docs.getdbt.com](https://docs.getdbt.com)
- **Dagger Docs**: [docs.dagger.io](https://docs.dagger.io)
- **GitHub Codespaces**: [docs.github.com/codespaces](https://docs.github.com/en/codespaces)

## 🎯 Benefits

### vs Local Development
- **Zero Setup**: No local Python/dbt/Dagster installation needed
- **Consistent Environment**: Same environment for all developers
- **Cloud Resources**: More compute power than typical local machines
- **Integrated Tooling**: Pre-configured VS Code with all extensions

### vs Traditional CI/CD
- **Local Testing**: Test CI pipeline locally before pushing
- **Faster Feedback**: No wait time for CI runners
- **Debugging**: Full terminal access during pipeline execution
- **Reproducible**: Same containerized environment everywhere

---

**Ready to develop!** Your Codespace provides a complete, production-ready development environment for modern data engineering with Dagster, dbt, and Snowflake. 🚀
