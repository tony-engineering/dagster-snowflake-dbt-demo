# Dagster + Snowflake + dbt Demo

[![Dagger CI](https://github.com/tony-engineering/dagster-snowflake-dbt-demo/actions/workflows/dagger-ci.yml/badge.svg)](https://github.com/tony-engineering/dagster-snowflake-dbt-demo/actions/workflows/dagger-ci.yml)

A modern data stack demonstration showcasing orchestration, transformation, and cloud data warehousing integration.

## What This Project Does

This project demonstrates a complete data pipeline using industry-standard tools:

- **🎯 Dagster**: Orchestrates data workflows and manages asset dependencies
- **🔄 dbt**: Transforms raw data into analytics-ready models using SQL
- **❄️ Snowflake**: Provides scalable cloud data warehouse for storage and compute

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Dagster   │───▶│     dbt     │───▶│  Snowflake  │
│ (Orchestration) │ │ (Transform) │    │ (Warehouse) │
│             │    │             │    │             │
│ - Asset mgmt│    │ - SQL models│    │ - Storage   │
│ - Scheduling│    │ - Tests     │    │ - Compute   │
│ - Monitoring│    │ - Docs      │    │ - Scaling   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Project Structure

```
dagster-snowflake-dbt-demo/
├── dagster-demo/          # Orchestration layer
│   └── dagster_demo/      # Dagster assets and jobs
├── dbt_demo/              # Data transformation layer
│   ├── models/            # SQL transformation models
│   └── dbt_project.yml    # dbt configuration
└── venv/                  # Python virtual environment
```

## Key Features

- **Unified Orchestration**: Dagster manages the entire data pipeline lifecycle
- **SQL-First Transformations**: dbt enables analytics engineers to build reliable data models
- **Cloud-Native**: Leverages Snowflake's elastic compute and storage
- **Data Quality**: Built-in testing and validation at every step
- **Observability**: Comprehensive monitoring and lineage tracking
- **Automated CI/CD**: Dagger-powered continuous integration with comprehensive testing

## CI/CD Pipeline

This project includes a robust CI/CD pipeline powered by Dagger that runs on every push and pull request:

- **🔍 Code Linting**: Black, Ruff, and isort for code quality
- **🧪 Testing**: Pytest for unit and integration tests
- **✅ Dagster Validation**: Ensures all assets and definitions load correctly
- **🔨 dbt Validation**: Validates SQL models and compilation
- **🛡️ Security Scanning**: Safety and Bandit for dependency and code security

The CI pipeline uses an in-memory DuckDB database for dbt validation, requiring no external dependencies.

## Getting Started

1. **Setup Environment**: Activate the Python virtual environment
2. **Configure Connections**: Ensure Snowflake credentials are properly configured
3. **Run Pipeline**: Execute data workflows through Dagster UI or CLI
4. **View Results**: Monitor pipeline execution and inspect transformed data

## Use Cases

This pattern is ideal for:
- **Analytics Engineering**: Building reliable data models for BI and reporting
- **Data Pipeline Automation**: Scheduling and monitoring data workflows
- **Data Quality Assurance**: Implementing tests and checks throughout the pipeline
- **Team Collaboration**: Enabling data teams to work with familiar SQL-based tools

## Technologies

- **Python 3.13+**: Runtime environment
- **Dagster**: Data orchestration platform
- **dbt**: Data transformation framework
- **Snowflake**: Cloud data platform
- **SQL**: Primary transformation language

---

*This demo showcases modern data engineering practices using open-source orchestration with enterprise-grade data infrastructure.*
