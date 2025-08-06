{{ config(materialized='table') }}

-- Simple example staging model
select 
    1 as customer_id,
    'John Doe' as customer_name,
    'john@example.com' as email,
    current_timestamp as created_date,
    'Premium' as customer_tier

union all

select 
    2 as customer_id,
    'Jane Smith' as customer_name, 
    'jane@example.com' as email,
    current_timestamp as created_date,
    'Standard' as customer_tier
