# Constants for yearly partitioning based on company founded years

# Date format for Dagster partition definitions - required even for yearly partitions
DATE_FORMAT = "%Y-%m-%d"

# Start and end dates for yearly partitions
# Dagster will create partitions like "2000-01-01", "2001-01-01", etc.
START_DATE = "2000-01-01"  # Start from year 2000 for modern companies
END_DATE = "2024-01-01"    # End at 2024 (note: YearlyPartitionsDefinition is end-exclusive)

# The FOUNDED field in our data is stored as integer years (2000, 2001, 2002, etc.)
# We'll extract the year from Dagster's partition key using context.partition_key[:4] or similar
