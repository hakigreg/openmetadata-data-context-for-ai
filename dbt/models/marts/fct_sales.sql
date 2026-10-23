select
    sale_line_id,
    invoice_id,
    customer_id,
    product_id,
    invoice_at,
    invoice_at::date as sale_date,
    date_trunc('month', invoice_at)::date as sale_month,
    billing_country,
    billing_state,
    billing_city,
    unit_price,
    quantity,
    extended_amount as revenue
from {{ ref('int_sales_enriched') }}
