import json

from websocket import create_connection

WS_URL = "wss://s-usc1c-nss-279.firebaseio.com/.ws?v=5&ns=otvoreni-radio-player"


# Reverse engineered from: www.otvoreni.hr/media-player/
def load():
    ws = create_connection(WS_URL)
    ws.recv()

    ws.send('{"t":"d","d":{"r":2,"a":"q","b":{"p":"/songs","h":""}}}')
    data = ws.recv()
    ws.close()

    data = json.loads(data)
    plays = data["d"]["b"]["d"]["8807"]
    key = list(plays)[-1]

    return (
        plays[key]["artist"].title(),
        plays[key]["title"].capitalize()
    )
