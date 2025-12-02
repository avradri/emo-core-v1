def test_import_core_packages() -> None:
    """
    Basic smoke test: make sure the main packages import cleanly.

    This is the first thing a lab tech lead or CI will hit.
    """
    import emo  # noqa: F401
    import emo.organismality  # noqa: F401
    import emo.synergy  # noqa: F401
    import emo.gwi  # noqa: F401
    import emo.smf  # noqa: F401
    import emo.info_time  # noqa: F401
    import emo.reciprocity  # noqa: F401
    import emo.uia_engine.aggregate  # noqa: F401

    # API and orchestration modules should also be importable
    import api  # noqa: F401
    import orchestration.prefect_flows  # noqa: F401
