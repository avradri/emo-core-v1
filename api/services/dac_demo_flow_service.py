from api.demo.romania_disaster_demo import (
    ROMANIA_DISASTER_DELIVERY,
    ROMANIA_DISASTER_DIAGNOSTIC,
    ROMANIA_DISASTER_POLICY,
)


def get_romania_disaster_demo_flow():
    return {
        "diagnostic": ROMANIA_DISASTER_DIAGNOSTIC,
        "policy": ROMANIA_DISASTER_POLICY,
        "delivery": ROMANIA_DISASTER_DELIVERY,
    }
