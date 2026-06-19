import time
import pytest

from lextrader.api.decision_service import DecisionService


def test_toggle_valid_id():
    svc = DecisionService()
    initial = next(a for a in svc._algorithms if a.id == "ensemble").is_active

    resp = svc.toggle("ensemble")
    assert resp.ok is True
    assert resp.algorithm_id == "ensemble"
    assert resp.is_active is (not initial)


def test_toggle_invalid_id():
    svc = DecisionService()
    resp = svc.toggle("does-not-exist")
    assert resp.ok is False
    assert resp.algorithm_id == "does-not-exist"


def test_run_sets_is_processing_and_finishes():
    svc = DecisionService()
    r1 = svc.run()
    assert r1.ok is True

    # Should be processing immediately
    state = svc.get_state()
    assert state.is_processing is True

    # Wait for simulation to finish (6 steps * 0.6s + 0.5s)
    time.sleep(4.5)

    state2 = svc.get_state()
    assert state2.is_processing is False
    assert len(state2.recent_decisions) >= 1


def test_run_is_blocked_while_processing():
    svc = DecisionService()
    svc.run()
    r2 = svc.run()
    assert r2.ok is False

