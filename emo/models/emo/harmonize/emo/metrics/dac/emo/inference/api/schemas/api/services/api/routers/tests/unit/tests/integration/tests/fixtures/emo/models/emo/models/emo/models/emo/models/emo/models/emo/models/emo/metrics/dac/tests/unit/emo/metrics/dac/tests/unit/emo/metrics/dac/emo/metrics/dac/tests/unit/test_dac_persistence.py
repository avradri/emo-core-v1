from emo.metrics.dac.persistence import (
    implementation_persistence_30d,
    implementation_persistence_90d,
)


def test_implementation_persistence_30d():
    assert implementation_persistence_30d(10, 7) == 0.7


def test_implementation_persistence_90d():
    assert implementation_persistence_90d(10, 5) == 0.5


def test_persistence_with_zero_started():
    assert implementation_persistence_30d(0, 0) is None
    assert implementation_persistence_90d(0, 0) is None
