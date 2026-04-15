from typing import List


def missing_required_fields(required_fields: List[str], present_fields: List[str]) -> List[str]:
    present = set(present_fields)
    return [field for field in required_fields if field not in present]
