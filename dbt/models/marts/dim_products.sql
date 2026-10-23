select
    track.track_id as product_id,
    track.track_name as product_name,
    album.album_title,
    artist.artist_name,
    genre.genre_name,
    track.composer,
    track.milliseconds as duration_ms,
    track.list_price
from {{ ref('stg_tracks') }} as track
left join {{ ref('stg_albums') }} as album using (album_id)
left join {{ ref('stg_artists') }} as artist using (artist_id)
left join {{ ref('stg_genres') }} as genre using (genre_id)
