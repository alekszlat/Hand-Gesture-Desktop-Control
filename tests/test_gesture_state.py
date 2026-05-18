"""Tests for gesture state helpers and state tracking."""

from gestures.gesture_state import GestureState
from gestures.gesture_state_tracker import GestureStateTracker


def test_gesture_state_transition_helpers():
    state = GestureState(
        name="Open_Palm",
        previous_name="Closed_Fist",
        confidence=0.95,
        duration=1.2,
        changed=True,
    )

    assert state.is_active is True
    assert state.was_changed is True
    assert state.is_gesture("Open_Palm") is True
    assert state.changed_to("Open_Palm") is True
    assert state.changed_from_to("Closed_Fist", "Open_Palm") is True
    assert state.held_for(1.0) is True


def test_gesture_state_tracker_records_changes_and_duration(monkeypatch):
    times = iter([10.0, 10.0, 11.5])
    monkeypatch.setattr("gestures.gesture_state_tracker.time.time", lambda: next(times))
    tracker = GestureStateTracker()

    first_state = tracker.update("Open_Palm", confidence=0.8)
    second_state = tracker.update("Open_Palm", confidence=0.9)

    assert first_state.changed is True
    assert first_state.previous_name is None
    assert second_state.changed is False
    assert second_state.duration == 1.5
    assert second_state.confidence == 0.9
