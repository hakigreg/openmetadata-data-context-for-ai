select
    customer_id,
    concat(first_name, ' ', last_name) as customer_name,
    company_name,
    email,
    city,
    state,
    country,
    postal_code,
    support_rep_id
from {{ ref('stg_customers') }}
