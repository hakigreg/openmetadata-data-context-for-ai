select
    customer.customer_id,
    customer.customer_name,
    customer.company_name,
    customer.country,
    customer.state,
    customer.city,
    min(sales.invoice_at) as first_purchase_at,
    max(sales.invoice_at) as latest_purchase_at,
    count(distinct sales.invoice_id) as order_count,
    sum(sales.quantity) as units_purchased,
    sum(sales.revenue)::numeric(14, 2) as lifetime_value,
    (sum(sales.revenue) / nullif(count(distinct sales.invoice_id), 0))::numeric(14, 2) as average_order_value
from {{ ref('dim_customers') }} as customer
left join {{ ref('fct_sales') }} as sales using (customer_id)
group by 1, 2, 3, 4, 5, 6
