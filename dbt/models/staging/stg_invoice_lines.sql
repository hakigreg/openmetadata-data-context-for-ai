select
    invoice_line_id,
    invoice_id,
    track_id,
    unit_price::numeric(12, 2) as unit_price,
    quantity::integer as quantity,
    (unit_price * quantity)::numeric(12, 2) as extended_amount
from {{ source('chinook', 'invoice_line') }}
