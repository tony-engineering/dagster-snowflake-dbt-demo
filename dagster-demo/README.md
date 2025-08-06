# Dagster dbt Integration Demo

This repository demonstrates how to integrate Dagster with dbt, enabling you to manage your dbt models as Dagster assets with full lineage, monitoring, and orchestration capabilities.

## 🏗️ Project Structure

```
dagster-snowflake-dbt-demo/
├── dagster-demo/                  # Dagster orchestration project
│   ├── src/dagster_demo/
│   │   ├── definitions.py         # Main Dagster definitions
│   │   └── defs/
│   │       ├── project.py         # dbt project configuration  
│   │       ├── resources.py       # Dagster resources (dbt CLI)
│   │       └── assets/
│   │           └── dbt.py         # dbt assets definition
│   ├── pyproject.toml             # Python dependencies
│   └── test_integration.py        # Integration test script
│
├── dbt_demo/                      # dbt transformation project
│   ├── dbt_project.yml           # dbt project configuration
│   ├── profiles.yml              # dbt profiles (DuckDB/Snowflake)
│   ├── models/example/           # dbt models
│   │   ├── my_first_dbt_model.sql
│   │   ├── my_second_dbt_model.sql
│   │   └── schema.yml
│   └── target/                   # dbt build artifacts (manifest.json)
│
└── data/                         # Database files (DuckDB)
    └── dbt_demo.duckdb
```

## 🚀 Key Components

### 1. dbt Project Configuration (`dbt_demo/dbt_project.yml`)
- Standard dbt project with example models
- Configured for both DuckDB (dev) and Snowflake (prod)

### 2. Dagster-dbt Integration Components

#### `defs/project.py` - dbt Project Setup
```python
from dagster_dbt import DbtProject

dbt_project = DbtProject(
    project_dir=Path(__file__).parent.parent.parent.parent.parent / "dbt_demo"
)
```

#### `defs/resources.py` - dbt CLI Resource
```python
from dagster_dbt import DbtCliResource

dbt_resource = DbtCliResource(
    project_dir=dbt_project,
)
```

#### `defs/assets/dbt.py` - dbt Assets Definition
```python
@dbt_assets(
    manifest=dbt_project.manifest_path,
)
def dbt_demo_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
```

### 3. Database Support
- **Development**: DuckDB (lightweight, local)
- **Production**: Snowflake (configured via environment variables)

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9+
- dbt-core
- Dagster

### 1. Install Dependencies
```bash
cd dagster-demo
pip install -e .
```

### 2. Parse dbt Project
```bash
cd ../dbt_demo
dbt parse --profiles-dir .
```

### 3. Test Integration
```bash
cd ../dagster-demo
python test_integration.py
```

### 4. Launch Dagster UI
```bash
dagster dev
```

Open http://localhost:3000 to access the Dagster UI.

## 🎯 Features Implemented

### ✅ Core Integration
- [x] dbt models as Dagster assets
- [x] Automatic lineage detection
- [x] dbt manifest parsing
- [x] Multi-environment support (dev/prod)

### ✅ Database Support  
- [x] DuckDB for development
- [x] Snowflake for production
- [x] Environment-based configuration

### ✅ Development Tools
- [x] Integration test script
- [x] Proper project structure
- [x] Comprehensive documentation

## 🔧 Configuration

### Environment Variables (for Snowflake)
```bash
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password" 
export SNOWFLAKE_ROLE="your-role"
export SNOWFLAKE_DATABASE="your-database"
export SNOWFLAKE_WAREHOUSE="your-warehouse"
export SNOWFLAKE_SCHEMA="your-schema"
```

### Development vs Production
- **Development**: Uses DuckDB with local file storage
- **Production**: Uses Snowflake with environment variables

## 📊 Usage

### 1. View Assets in Dagster UI
- Navigate to the "Assets" tab
- See your dbt models as Dagster assets
- View lineage and dependencies

### 2. Materialize Assets
- Click "Materialize all" to run all dbt models
- Or select specific assets to run

### 3. Monitor Execution
- View run logs and status
- Track data lineage
- Monitor performance metrics

## 🧪 Testing

Run the integration test to verify everything is working:
```bash
python test_integration.py
```

Expected output:
```
🚀 Testing Dagster dbt Integration
==================================================
✅ Successfully imported Dagster definitions  
✅ dbt_project.yml found
✅ dbt manifest.json found
✅ Found 2 assets:
   - AssetKey(['my_first_dbt_model'])
   - AssetKey(['my_second_dbt_model'])
==================================================
🎉 Integration test completed successfully!
```

## 🔄 Development Workflow

1. **Modify dbt models** in `dbt_demo/models/`
2. **Parse dbt project**: `cd dbt_demo && dbt parse --profiles-dir .`
3. **Reload Dagster**: The UI will automatically detect changes
4. **Test changes**: Run materialization in Dagster UI

## 🚀 Next Steps

- Add more complex dbt models with sources and transformations  
- Implement data quality tests
- Add scheduling and sensors
- Integrate with data cataloging tools
- Add monitoring and alerting

## 🎓 Learning Resources

- [Dagster dbt Integration Guide](https://docs.dagster.io/integrations/dbt)
- [dbt Documentation](https://docs.getdbt.com/)
- [Dagster Concepts](https://docs.dagster.io/concepts)

## 🤝 Contributing

Feel free to extend this demo with additional features or improvements!

# dagster_demo

This is a [Dagster](https://dagster.io/) project scaffolded with [`dagster project scaffold`](https://docs.dagster.io/guides/build/projects/creating-a-new-project).

## Getting started

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `dagster_demo/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.

## Development

### Adding new Python dependencies

You can specify new Python dependencies in `setup.py`.

### Unit testing

Tests are in the `dagster_demo_tests` directory and you can run tests using `pytest`:

```bash
pytest dagster_demo_tests
```

### Schedules and sensors

If you want to enable Dagster [Schedules](https://docs.dagster.io/guides/automate/schedules/) or [Sensors](https://docs.dagster.io/guides/automate/sensors/) for your jobs, the [Dagster Daemon](https://docs.dagster.io/guides/deploy/execution/dagster-daemon) process must be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and sensors for your jobs.

## Deploy on Dagster+

The easiest way to deploy your Dagster project is to use Dagster+.

Check out the [Dagster+ documentation](https://docs.dagster.io/dagster-plus/) to learn more.
