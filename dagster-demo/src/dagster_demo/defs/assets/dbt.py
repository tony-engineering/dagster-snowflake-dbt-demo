import dagster as dg
from dagster_dbt import DbtCliResource, dbt_assets

from dagster_demo.defs.project import dbt_project


@dbt_assets(
    manifest=dbt_project.manifest_path,
    exclude="stg_french_companies_by_year french_tech_companies_summary",  # Exclude partitioned models
)
def dbt_demo_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    """
    Define dbt models as Dagster assets.
    This will create assets for all dbt models in your project except partitioned ones.
    """
    yield from dbt.cli(
        [
            "build",
            "--exclude",
            "stg_french_companies_by_year",
            "--exclude",
            "french_tech_companies_summary",
        ],
        context=context,
    ).stream()
