from pathlib import Path

from dagster import Definitions
from dagster_demo.defs.assets.dbt import dbt_demo_assets
from dagster_demo.defs.assets.partitioned_dbt_assets import (
    partitioned_french_companies_dbt_assets,
    summary_dbt_assets
)
from dagster_demo.defs.resources import dbt_resource


defs = Definitions(
    assets=[
        dbt_demo_assets, 
        partitioned_french_companies_dbt_assets,
        summary_dbt_assets
    ],
    resources={"dbt": dbt_resource},
)
