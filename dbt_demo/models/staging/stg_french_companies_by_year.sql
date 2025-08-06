{{ config(materialized='table') }}

-- French companies in data-related technology industries - partitioned by founded year
-- This model will be materialized as a partitioned asset in Dagster
-- Handles both single partition and multi-partition backfill scenarios

{% set partition_year = var('partition_year', none) %}
{% set partition_years_list = var('partition_years_list', none) %}

with french_data_companies as (
    select 
        name as company_name,
        industry,
        locality,
        region,
        size as company_size,
        founded as founded_year,
        website,
        id as company_id,
        linkedin_url
    from {{ source('my_company_data', 'freecompanydataset') }}
    where 
        country = 'france'
        and industry in (
            'computer software',
            'information technology and services', 
            'computer & network security'
        )
        and name is not null
        {% if partition_years_list %}
        and founded in {{ partition_years_list }}  -- Backfill multiple years
        {% elif partition_year %}
        and founded = {{ partition_year }}  -- Single partition
        {% else %}
        and founded = 2024  -- Default fallback
        {% endif %}
)

select 
    company_id,
    company_name,
    industry,
    locality,
    region,
    company_size,
    founded_year,
    website,
    linkedin_url,
    case 
        when founded_year >= 2010 then 'Startup Era'
        when founded_year >= 2000 then 'Dot-com Era'
        when founded_year >= 1990 then 'PC Era'
        when founded_year is not null then 'Legacy'
        else 'Unknown'
    end as company_era,
    case
        when company_size in ('1-10') then 'Micro'
        when company_size in ('11-50') then 'Small'
        when company_size in ('51-200') then 'Medium'
        when company_size in ('201-500', '501-1000') then 'Large'
        when company_size in ('1001-5000', '5001-10000', '10000+') then 'Enterprise'
        else 'Unknown'
    end as size_category,
    {% if partition_years_list %}
    founded_year as partition_year  -- Use actual founded year for backfills
    {% else %}
    {{ partition_year }} as partition_year  -- Use provided partition year for single runs
    {% endif %}
from french_data_companies
order by company_name
