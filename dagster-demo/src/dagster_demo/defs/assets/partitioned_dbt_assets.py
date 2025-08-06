import dagster as dg
from dagster_dbt import DbtCliResource, dbt_assets

from dagster_demo.defs.project import dbt_project
from dagster_demo.defs.partitions import yearly_partition


@dbt_assets(
    manifest=dbt_project.manifest_path,
    partitions_def=yearly_partition,
    select="stg_french_companies_by_year"  # Only build the partitioned model
)
def partitioned_french_companies_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    """
    Partitioned dbt assets for French tech companies by founded year.
    Each partition processes companies founded in a specific year.
    """
    # Extract the year from the partition key (e.g., "2020" -> "2020")
    partition_year = context.partition_key
    
    # Run dbt with the partition_year variable
    yield from dbt.cli(
        ["build", "--select", "stg_french_companies_by_year", "--vars", f"partition_year: {partition_year}"], 
        context=context
    ).stream()


# Summary dbt asset that depends on partitioned data
@dbt_assets(
    manifest=dbt_project.manifest_path,
    select="french_tech_companies_summary"
)
def summary_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    """
    Summary dbt model that aggregates data from all partitioned French companies.
    Dependencies are handled through dbt's ref() function in the SQL.
    """
    yield from dbt.cli(["build", "--select", "french_tech_companies_summary"], context=context).stream()
