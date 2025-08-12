import dagster as dg
from dagster_dbt import DbtCliResource, dbt_assets

from dagster_demo.defs.partitions import yearly_partition
from dagster_demo.defs.project import dbt_project


@dbt_assets(
    manifest=dbt_project.manifest_path,
    partitions_def=yearly_partition,
    select="stg_french_companies_by_year",  # Only build the partitioned model
)
def partitioned_french_companies_dbt_assets(
    context: dg.AssetExecutionContext, dbt: DbtCliResource
):
    """
    Partitioned dbt assets for French tech companies by founded year.
    Standard approach: each partition runs separately during backfills.
    """
    # Use partition_keys which works for both single and multi-partition scenarios
    partition_keys = context.partition_keys

    if len(partition_keys) == 1:
        # Single partition run
        partition_year = partition_keys[0]
        context.log.info(f"Processing single partition for year: {partition_year}")

        yield from dbt.cli(
            [
                "build",
                "--select",
                "stg_french_companies_by_year",
                "--vars",
                f"partition_year: {partition_year}",
            ],
            context=context,
        ).stream()
    else:
        # Multiple partitions in backfill - process all years in one dbt run
        context.log.info(
            f"Processing backfill for {len(partition_keys)} partitions: {partition_keys}"
        )

        # Create SQL IN clause format: (2020,2021,2022)
        years_sql = "(" + ",".join(partition_keys) + ")"
        context.log.info(f"Running dbt with years filter: founded IN {years_sql}")

        yield from dbt.cli(
            [
                "build",
                "--select",
                "stg_french_companies_by_year",
                "--vars",
                f"partition_years_list: {years_sql}",
            ],
            context=context,
        ).stream()


# Summary dbt asset that depends on partitioned data
@dbt_assets(manifest=dbt_project.manifest_path, select="french_tech_companies_summary")
def summary_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    """
    Summary dbt model that aggregates data from all partitioned French companies.
    Dependencies are handled through dbt's ref() function in the SQL.
    """
    yield from dbt.cli(
        ["build", "--select", "french_tech_companies_summary"], context=context
    ).stream()
