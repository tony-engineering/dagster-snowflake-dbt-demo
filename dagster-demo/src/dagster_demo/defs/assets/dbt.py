from pathlib import Path

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

# Path to your dbt project
DBT_PROJECT_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "dbt_demo"
DBT_MANIFEST_PATH = DBT_PROJECT_PATH / "target" / "manifest.json"

@dbt_assets(manifest=DBT_MANIFEST_PATH)
def dbt_demo_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    Define dbt models as Dagster assets.
    This will create assets for all dbt models in your project.
    """
    yield from dbt.cli(["build"], context=context).stream()
