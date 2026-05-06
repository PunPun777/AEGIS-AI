_previous_tes: dict[str, float] = {}

def get_trend(region: str, current_tes: float) -> str:
    previous = _previous_tes.get(region)
    _previous_tes[region] = current_tes

    if previous is None:
        return "stable"
    if current_tes > previous:
        return "increasing"
    if current_tes < previous:
        return "decreasing"
    return "stable"
