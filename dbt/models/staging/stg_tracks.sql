select
    track_id,
    trim(name) as track_name,
    album_id,
    genre_id,
    media_type_id,
    composer,
    milliseconds,
    bytes,
    unit_price::numeric(12, 2) as list_price
from {{ source('chinook', 'track') }}
