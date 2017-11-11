import re

# A list of artists which feature a hyphen in their name
hyphenated_artists = [
    "A-Ha",
    "Alt-J",
    "T-Rex",
    "In-Grid",
    "Jay-Z",
]


def split_artist_title(string, normalize_case=False):
    # Remove whitespace and underscores
    string = string.replace("_", " ").strip()

    # Try splitting by hyphen surrounded by whitespace
    bits = re.split('\\s+-\\s+', string, 1)

    # Try with only one space from any side (radio student does this)
    if len(bits) < 2:
        bits = re.split('-\\s+', string, 1)

    if len(bits) < 2:
        bits = re.split('\\s+-', string, 1)

    # Check for known hyphenated authors
    if len(bits) < 2:
        for artist in hyphenated_artists:
            if re.match("^{}\\s*-".format(artist), string, re.I):
                bits = [
                    string[0:len(artist)].strip('- '),
                    string[len(artist):].strip('- '),
                ]
                break

    # Last resort - split by hyphen without spaces
    if len(bits) < 2:
        bits = string.split('-', 1)

    # Failed :/
    if len(bits) < 2:
        return None

    if normalize_case:
        return [bits[0].title(), bits[1].capitalize()]

    return bits
