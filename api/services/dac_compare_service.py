from api.schemas.dac_compare import DACCompareResponse, DACCompareSide


def get_dac_compare() -> DACCompareResponse:
    return DACCompareResponse(
        left=DACCompareSide(
            jurisdiction="RO",
            warning_to_policy_lag_days=3,
            declared_vs_funded_gap=0.2,
        ),
        right=DACCompareSide(
            jurisdiction="BG",
            warning_to_policy_lag_days=5,
            declared_vs_funded_gap=0.3,
        ),
    )
