import dagster as dg
from dagster_dbt import DbtCliResource

from dagster_demo.defs.project import dbt_project

# Create dbt resource using the dbt_project
dbt_resource = DbtCliResource(
    project_dir=dbt_project,
)

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "dbt": dbt_resource,
        },
    )
