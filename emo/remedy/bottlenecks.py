from __future__ import annotations

from emo.models.bottleneck_profile import BottleneckProfile

BOTTLENECK_KEYS = (
    "validation",
    "translation",
    "budget",
    "deployment",
    "persistence",
    "contradiction",
)


def _clamp_score(value: float | int | None) -> float:
    if value is None:
        return 0.0
    return max(0.0, min(float(value), 1.0))


def classify_bottlenecks(
    *,
    domain: str,
    jurisdiction: str,
    validation_score: float | int | None,
    translation_score: float | int | None,
    budget_score: float | int | None,
    deployment_score: float | int | None,
    persistence_score: float | int | None,
    contradiction_score: float | int | None,
) -> BottleneckProfile:
    """
    Build a first-pass RDL bottleneck profile from DAC-style sub-scores.

    Convention:
    - higher validation / translation / budget / deployment / persistence = stronger performance
    - higher contradiction = worse contradiction burden

    Dominant bottlenecks are the weakest positive pipeline stages plus contradiction
    when contradiction is materially high.
    """
    scores = {
        "validation": _clamp_score(validation_score),
        "translation": _clamp_score(translation_score),
        "budget": _clamp_score(budget_score),
        "deployment": _clamp_score(deployment_score),
        "persistence": _clamp_score(persistence_score),
        "contradiction": _clamp_score(contradiction_score),
    }

    positive_pipeline = {
        "validation": scores["validation"],
        "translation": scores["translation"],
        "budget": scores["budget"],
        "deployment": scores["deployment"],
        "persistence": scores["persistence"],
    }

    min_positive = min(positive_pipeline.values())
    dominant_bottlenecks = [
        name for name, value in positive_pipeline.items() if value == min_positive
    ]

    if scores["contradiction"] >= 0.6:
        dominant_bottlenecks.append("contradiction")

    spread = max(positive_pipeline.values()) - min_positive
    confidence = round(min(1.0, 0.55 + spread / 2.0), 3)

    return BottleneckProfile(
        domain=domain,
        jurisdiction=jurisdiction,
        validation_score=scores["validation"],
        translation_score=scores["translation"],
        budget_score=scores["budget"],
        deployment_score=scores["deployment"],
        persistence_score=scores["persistence"],
        contradiction_score=scores["contradiction"],
        dominant_bottlenecks=dominant_bottlenecks,
        confidence=confidence,
    )
