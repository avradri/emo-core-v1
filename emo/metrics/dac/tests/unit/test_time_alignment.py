from emo.harmonize.time_alignment import parse_iso_datetime


def test_parse_iso_datetime_valid():
    result = parse_iso_datetime("2026-01-01T12:30:00")
    assert result is not None
    assert result.year == 2026
    assert result.month == 1
    assert result.day == 1


def test_parse_iso_datetime_none():
    assert parse_iso_datetime(None) is None
