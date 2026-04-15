from emo.harmonize.jurisdiction_mapping import normalize_jurisdiction


def test_normalize_jurisdiction_uppercases_and_strips():
    assert normalize_jurisdiction(" ro ") == "RO"
    assert normalize_jurisdiction("eu") == "EU"


def test_normalize_jurisdiction_none():
    assert normalize_jurisdiction(None) is None
