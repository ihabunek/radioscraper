async def load(session):
    url = "https://otvoreni.hr/umbraco/Surface/NowPlayingSurface/GetNowPlaying?stream=otvoreni"
    response = await session.get(url)
    data = await response.json()

    return (
        data["artist"].title(),
        data["title"].capitalize()
    )
