# Dagster Snowflake dbt Demo

A complete development environment for building data pipelines with Dagster, Snowflake, and dbt using GitHub Codespaces.

## 🚀 Quick Start with GitHub Codespaces

1. **Fork or clone this repository**
2. **Open in Codespaces**: 
   - Click the green "Code" button
   - Select "Codespaces" tab
   - Click "Create codespace on main"
3. **Wait for setup**: The devcontainer will automatically install all dependencies
4. **Configure your environment** (see Configuration section below)

## 🏗️ What's Included

### Tools & Frameworks
- **Dagster**: Modern data orchestration platform
- **dbt**: Transform data in your warehouse
- **Snowflake**: Cloud data warehouse connector
- **Python 3.11**: Latest Python with data science libraries
- **Jupyter Lab**: Interactive development environment
- **Streamlit**: Build data apps quickly

### VS Code Extensions
- Python development tools (Black, isort, flake8)
- dbt Power User for dbt development
- GitHub Copilot for AI assistance
- YAML and JSON support

### Pre-configured Ports
- `3000`: Dagster Web UI
- `8080`: Alternative web services
- `8501`: Streamlit applications

## ⚙️ Configuration

### 1. Environment Variables
Create a `.env` file in the root directory:

```bash
# Snowflake Configuration
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_ROLE=your_role

# Optional: Additional configurations
DAGSTER_HOME=/opt/dagster/dagster_home
DBT_PROFILES_DIR=/workspaces/dagster-snowflake-dbt-demo/.dbt
```

### 2. dbt Profile Configuration
Create `.dbt/profiles.yml`:

```yaml
dagster_snowflake_dbt_demo:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
      schema: "{{ env_var('SNOWFLAKE_SCHEMA') }}"
      threads: 4
      client_session_keep_alive: False
```

## 🛠️ Development Workflow

### Start Dagster Development Server
```bash
dagster dev
```
Access the Dagster UI at `http://localhost:3000`

### Work with dbt
```bash
# Initialize dbt project
dbt init my_dbt_project

# Install dbt packages
dbt deps

# Run dbt models
dbt run

# Test dbt models
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

### Launch Jupyter Lab
```bash
jupyter lab
```

### Run Streamlit Apps
```bash
streamlit run app.py
```

## 📁 Project Structure

```
dagster-snowflake-dbt-demo/
├── .devcontainer/
│   ├── devcontainer.json      # Codespaces configuration
│   └── setup.sh              # Environment setup script
├── .dbt/                     # dbt profiles directory
├── dagster_project/          # Dagster assets and resources
├── dbt_project/             # dbt models and transformations
├── data/                    # Sample data files
├── tests/                   # Test files
├── .env                     # Environment variables (create this)
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Python project configuration
└── README.md               # This file
```

## 🔧 Customization

### Adding New Python Packages
Add to `requirements.txt` and run:
```bash
pip install -r requirements.txt
```

### Modifying VS Code Settings
Edit `.devcontainer/devcontainer.json` and rebuild the container.

### Adding System Dependencies
Modify `.devcontainer/setup.sh` and rebuild the container.

## 🚨 Security Notes

- Never commit `.env` files with real credentials
- Use GitHub Secrets for production deployments
- Rotate Snowflake credentials regularly
- Consider using Snowflake key-pair authentication for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test in Codespaces
5. Submit a pull request

## 📚 Resources

- [Dagster Documentation](https://docs.dagster.io/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)

## 🐛 Troubleshooting

### Container won't start
- Check `.devcontainer/devcontainer.json` syntax
- Verify all file paths are correct
- Look at the setup logs in Codespaces

### Snowflake connection issues
- Verify credentials in `.env` file
- Check network connectivity
- Ensure Snowflake account is accessible

### dbt errors
- Verify `profiles.yml` configuration
- Check dbt version compatibility
- Ensure Snowflake permissions are correct

---

Happy coding! 🎉
