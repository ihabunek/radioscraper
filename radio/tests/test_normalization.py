from radio.utils.normalize import split_artist_title


def test_split_artist_title():
    expected = {
        "foo-bar": ["foo", "bar"],
        "foo-bar-baz": ["foo", "bar-baz"],
        "foo-bar - baz": ["foo-bar", "baz"],
        "foo-bar   -   baz": ["foo-bar", "baz"],
        "foo-bar- baz": ["foo-bar", "baz"],
        "foo-bar-  baz": ["foo-bar", "baz"],
        "foo-bar -baz": ["foo-bar", "baz"],
        "foo-bar  -baz": ["foo-bar", "baz"],
        "a-ha - take on me": ["a-ha", "take on me"],
        "a-ha-take on me": ["a-ha", "take on me"],
        "the beatles - hey jude": ["the beatles", "hey jude"],
    }

    for k, v in expected.items():
        assert split_artist_title(k) == v


def test_split_artist_title_normalize_case():
    expected = {
        "foo-bar": ["Foo", "Bar"],
        "foo-bar-baz": ["Foo", "Bar-baz"],
        "foo-bar - baz": ["Foo-Bar", "Baz"],
        "foo-bar- baz": ["Foo-Bar", "Baz"],
        "foo-bar -baz": ["Foo-Bar", "Baz"],
        "a-ha - take on me": ["A-Ha", "Take on me"],
        "a-ha-take on me": ["A-Ha", "Take on me"],
        "a-ha -take on me": ["A-Ha", "Take on me"],
        "a-ha- take on me": ["A-Ha", "Take on me"],
        "the beatles - hey jude": ["The Beatles", "Hey jude"],
    }

    for k, v in expected.items():
        assert split_artist_title(k, normalize_case=True) == v
