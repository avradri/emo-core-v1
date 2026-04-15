from emo.harmonize.quality_flags import missing_required_fields


def test_missing_required_fields_returns_missing_items():
    required = ["id", "domain", "source", "issued_at"]
    present = ["id", "domain"]

    result = missing_required_fields(required, present)

    assert result == ["source", "issued_at"]


def test_missing_required_fields_returns_empty_list_when_complete():
    required = ["id", "domain"]
    present = ["id", "domain"]

    result = missing_required_fields(required, present)

    assert result == []
