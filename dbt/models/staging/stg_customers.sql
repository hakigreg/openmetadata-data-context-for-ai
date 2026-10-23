select
    customer_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    nullif(trim(company), '') as company_name,
    nullif(trim(city), '') as city,
    nullif(trim(state), '') as state,
    nullif(trim(country), '') as country,
    nullif(trim(postal_code), '') as postal_code,
    lower(trim(email)) as email,
    support_rep_id
from {{ source('chinook', 'customer') }}
