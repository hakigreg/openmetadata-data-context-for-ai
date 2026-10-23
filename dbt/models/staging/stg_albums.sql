select album_id, trim(title) as album_title, artist_id
from {{ source('chinook', 'album') }}
