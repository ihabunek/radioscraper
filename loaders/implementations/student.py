from radio.utils.normalize import split_artist_title


async def load(session):
    url = 'http://www.radiostudent.hr/wp-admin/admin-ajax.php'

    response = await session.get(url, params={"action": "rsplaylist_api"})
    data = await response.json()
    artist_title = data['rows'][0]['played_song']

    return split_artist_title(artist_title)
