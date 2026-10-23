select
    line.invoice_line_id as sale_line_id,
    invoice.invoice_id,
    invoice.customer_id,
    line.track_id as product_id,
    invoice.invoice_at,
    invoice.billing_country,
    invoice.billing_state,
    invoice.billing_city,
    line.unit_price,
    line.quantity,
    line.extended_amount
from {{ ref('stg_invoice_lines') }} as line
inner join {{ ref('stg_invoices') }} as invoice using (invoice_id)
