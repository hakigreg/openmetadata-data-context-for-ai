select artist_id, trim(name) as artist_name
from {{ source('chinook', 'artist') }}
