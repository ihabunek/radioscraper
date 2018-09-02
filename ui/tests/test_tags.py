from ui.templatetags.radio import human_format


def test_human_format():
    assert human_format(-1) == '-1'
    assert human_format(0) == '0'
    assert human_format(1) == '1'
    assert human_format(1.53) == '1.5'
    assert human_format(10) == '10'
    assert human_format(100) == '100'
    assert human_format(1000) == '1K'
    assert human_format(1300) == '1.3K'
    assert human_format(1345) == '1.3K'
    assert human_format(1300000) == '1.3M'
    assert human_format(1950) == '1.9K'
    assert human_format(2147483647) == '2.1G'
    assert human_format(5000) == '5K'
    assert human_format(607593321) == '607.6M'
