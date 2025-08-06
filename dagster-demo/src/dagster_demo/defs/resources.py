from pathlib import Path

import dagster as dg
from dagster_dbt import DbtCliResource

# Path to your dbt project
DBT_PROJECT_PATH = Path(__file__).parent.parent.parent.parent.parent / "dbt_demo"

@dg.definitions
def resources():
    return dg.Definitions(resources={"dbt": dbt_resource})

dbt_resource = DbtCliResource(
    project_dir=str(DBT_PROJECT_PATH)
)
