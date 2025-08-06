{{ config(materialized='table') }}

-- Summary of French tech companies across all years
-- This aggregates data from the partitioned stg_french_companies_by_year tables

with yearly_stats as (
    select 
        partition_year,
        count(*) as total_companies,
        count(distinct industry) as unique_industries,
        count(distinct locality) as unique_locations,
        count(case when size_category = 'Micro' then 1 end) as micro_companies,
        count(case when size_category = 'Small' then 1 end) as small_companies,
        count(case when size_category = 'Medium' then 1 end) as medium_companies,
        count(case when size_category = 'Large' then 1 end) as large_companies,
        count(case when size_category = 'Enterprise' then 1 end) as enterprise_companies,
        count(case when company_era = 'Startup Era' then 1 end) as startup_era_count,
        count(case when company_era = 'Dot-com Era' then 1 end) as dotcom_era_count,
        count(case when company_era = 'PC Era' then 1 end) as pc_era_count,
        round(count(case when website is not null then 1 end) * 100.0 / count(*), 2) as website_percentage,
        round(count(case when linkedin_url is not null then 1 end) * 100.0 / count(*), 2) as linkedin_percentage
    from {{ ref('stg_french_companies_by_year') }}
    group by partition_year
),

overall_summary as (
    select
        count(distinct partition_year) as years_covered,
        sum(total_companies) as total_companies_all_years,
        sum(micro_companies) as total_micro_companies,
        sum(small_companies) as total_small_companies,
        sum(medium_companies) as total_medium_companies,
        sum(large_companies) as total_large_companies,
        sum(enterprise_companies) as total_enterprise_companies,
        avg(website_percentage) as avg_website_percentage,
        avg(linkedin_percentage) as avg_linkedin_percentage,
        min(partition_year) as earliest_year,
        max(partition_year) as latest_year,
        current_timestamp() as summary_created_at
    from yearly_stats
)

-- Return both yearly breakdown and overall summary
select 
    'yearly' as summary_type,
    partition_year::string as period,
    total_companies,
    unique_industries,
    unique_locations,
    micro_companies,
    small_companies,
    medium_companies,
    large_companies,
    enterprise_companies,
    startup_era_count,
    dotcom_era_count,
    pc_era_count,
    website_percentage,
    linkedin_percentage,
    null::timestamp as summary_created_at
from yearly_stats

union all

select 
    'overall' as summary_type,
    'all_years' as period,
    total_companies_all_years::integer as total_companies,
    null::integer as unique_industries,
    null::integer as unique_locations,
    total_micro_companies::integer as micro_companies,
    total_small_companies::integer as small_companies,
    total_medium_companies::integer as medium_companies,
    total_large_companies::integer as large_companies,
    total_enterprise_companies::integer as enterprise_companies,
    null::integer as startup_era_count,
    null::integer as dotcom_era_count,
    null::integer as pc_era_count,
    avg_website_percentage as website_percentage,
    avg_linkedin_percentage as linkedin_percentage,
    summary_created_at
from overall_summary

order by summary_type, period
