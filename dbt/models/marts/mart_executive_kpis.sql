select
    count(distinct invoice_id) as total_orders,
    count(distinct customer_id) as total_customers,
    sum(quantity) as total_units_sold,
    sum(revenue)::numeric(14, 2) as total_revenue,
    (sum(revenue) / nullif(count(distinct invoice_id), 0))::numeric(14, 2) as average_order_value,
    min(invoice_at) as reporting_period_start,
    max(invoice_at) as reporting_period_end
from {{ ref('fct_sales') }}
