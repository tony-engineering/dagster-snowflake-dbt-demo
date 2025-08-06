from pathlib import Path

from dagster_dbt import DbtProject

# Create a DbtProject instance pointing to the dbt_demo directory
dbt_project = DbtProject(
    project_dir=Path(__file__).parent.parent.parent.parent.parent / "dbt_demo"
)
