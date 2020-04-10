from radioscraper.utils import http


def load():
    url = "https://otvoreni-radio-player.firebaseio.com/songs/.json"
    response = http.get(url).json()

    plays = response["8807"]
    latest_timestamp = max(plays, key=int)
    play = plays[latest_timestamp]

    return (
        play["artist"].title(),
        play["title"].capitalize()
    )
