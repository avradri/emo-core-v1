from tests.fixtures.disaster_domain_profile import DISASTER_DOMAIN_PROFILE
from tests.fixtures.pandemic_domain_profile import PANDEMIC_DOMAIN_PROFILE


def test_disaster_domain_profile_name():
    assert DISASTER_DOMAIN_PROFILE.domain == "disaster"


def test_pandemic_domain_profile_name():
    assert PANDEMIC_DOMAIN_PROFILE.domain == "pandemic"


def test_domain_profiles_have_weighting_scheme():
    assert "lag" in DISASTER_DOMAIN_PROFILE.weighting_scheme
    assert "lag" in PANDEMIC_DOMAIN_PROFILE.weighting_scheme
