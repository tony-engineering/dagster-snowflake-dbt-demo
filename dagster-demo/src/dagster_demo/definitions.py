from pathlib import Path

from dagster import Definitions
from dagster_demo.defs.assets.dbt import dbt_demo_assets
from dagster_demo.defs.resources import dbt_resource


defs = Definitions(
    assets=[dbt_demo_assets],
    resources={"dbt": dbt_resource},
)
