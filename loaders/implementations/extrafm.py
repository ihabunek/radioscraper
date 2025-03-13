from radio.utils.normalize import split_artist_title


async def load(session):
    response = await session.get("https://streaming.extrafm.hr/stream/info/listen_extra_aac_.txt")
    contents = await response.text()
    return split_artist_title(contents, normalize_case=True)
