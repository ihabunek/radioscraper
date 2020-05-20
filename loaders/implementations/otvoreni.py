async def load(session):
    url = "https://otvoreni-radio-player.firebaseio.com/songs/.json"
    response = await session.get(url)
    contents = await response.json()

    plays = contents["8807"]
    latest_timestamp = max(plays, key=int)
    play = plays[latest_timestamp]

    return (
        play["artist"].title(),
        play["title"].capitalize()
    )
