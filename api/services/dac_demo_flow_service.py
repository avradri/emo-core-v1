from api.demo.bulgaria_disaster_demo import (
    BULGARIA_DISASTER_DELIVERY,
    BULGARIA_DISASTER_DIAGNOSTIC,
    BULGARIA_DISASTER_POLICY,
)
from api.demo.romania_disaster_demo import (
    ROMANIA_DISASTER_DELIVERY,
    ROMANIA_DISASTER_DIAGNOSTIC,
    ROMANIA_DISASTER_POLICY,
)


def get_disaster_compare_demo_flows():
    return {
        "left": {
            "diagnostic": ROMANIA_DISASTER_DIAGNOSTIC,
            "policy": ROMANIA_DISASTER_POLICY,
            "delivery": ROMANIA_DISASTER_DELIVERY,
        },
        "right": {
            "diagnostic": BULGARIA_DISASTER_DIAGNOSTIC,
            "policy": BULGARIA_DISASTER_POLICY,
            "delivery": BULGARIA_DISASTER_DELIVERY,
        },
    }
