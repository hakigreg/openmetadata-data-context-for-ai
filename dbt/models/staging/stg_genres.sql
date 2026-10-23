select genre_id, trim(name) as genre_name
from {{ source('chinook', 'genre') }}
