select
    product.product_id,
    product.product_name,
    product.album_title,
    product.artist_name,
    product.genre_name,
    count(distinct sales.invoice_id) as order_count,
    count(distinct sales.customer_id) as unique_customers,
    coalesce(sum(sales.quantity), 0) as units_sold,
    coalesce(sum(sales.revenue), 0)::numeric(14, 2) as revenue
from {{ ref('dim_products') }} as product
left join {{ ref('fct_sales') }} as sales using (product_id)
group by 1, 2, 3, 4, 5
