select
    sale_month,
    billing_country,
    count(distinct invoice_id) as order_count,
    count(distinct customer_id) as active_customers,
    sum(quantity) as units_sold,
    sum(revenue)::numeric(14, 2) as revenue,
    (sum(revenue) / nullif(count(distinct invoice_id), 0))::numeric(14, 2) as average_order_value
from {{ ref('fct_sales') }}
group by 1, 2
