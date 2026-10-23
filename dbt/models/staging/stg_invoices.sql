select
    invoice_id,
    customer_id,
    invoice_date::timestamp as invoice_at,
    nullif(trim(billing_city), '') as billing_city,
    nullif(trim(billing_state), '') as billing_state,
    nullif(trim(billing_country), '') as billing_country,
    nullif(trim(billing_postal_code), '') as billing_postal_code,
    total::numeric(12, 2) as invoice_total
from {{ source('chinook', 'invoice') }}
