from emo.metrics.dac.contradiction import declared_vs_funded_gap


def test_declared_vs_funded_gap():
    assert declared_vs_funded_gap(10, 6) == 0.4


def test_declared_vs_funded_gap_zero_declared():
    assert declared_vs_funded_gap(0, 0) is None
