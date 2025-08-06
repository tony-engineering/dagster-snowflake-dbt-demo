import dagster as dg
from datetime import datetime
from dagster_demo.defs.assets import constants

start_date = constants.START_DATE
end_date = constants.END_DATE

# Yearly partitions for company data based on founded year
# Using TimeWindowPartitionsDefinition with yearly cron schedule
yearly_partition = dg.TimeWindowPartitionsDefinition(
    start=datetime(2000, 1, 1),
    end=datetime(2025, 1, 1),
    cron_schedule="0 0 1 1 *",  # January 1st each year at midnight
    fmt="%Y"  # Format partition keys as years (e.g., "2020", "2021")
)
