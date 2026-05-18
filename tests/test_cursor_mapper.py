"""Tests for cursor mapping without a camera or real landmarks."""

from dataclasses import dataclass

from gestures.cursor_mapper import CursorMapper


@dataclass
class Landmark:
    x: float
    y: float


class Result:
    def __init__(self, hand_landmarks):
        self.hand_landmarks = hand_landmarks


def make_result(*landmarks):
    return Result(hand_landmarks=[list(landmarks)])


def test_maps_normalized_landmark_to_screen_position(monkeypatch):
    monkeypatch.setattr("gestures.cursor_mapper.time.time", lambda: 10.0)
    mapper = CursorMapper(
        screen_width=100,
        screen_height=50,
        cursor_landmark_index=0,
        mouse_update_interval=0.0,
        deadzone_pixels=0,
    )

    position = mapper.map_to_screen(make_result(Landmark(0.5, 0.5)))

    assert position == (50, 24)


def test_mirror_x_flips_horizontal_position(monkeypatch):
    monkeypatch.setattr("gestures.cursor_mapper.time.time", lambda: 10.0)
    mapper = CursorMapper(
        screen_width=100,
        screen_height=50,
        cursor_landmark_index=0,
        mouse_update_interval=0.0,
        mirror_x=True,
        deadzone_pixels=0,
    )

    position = mapper.map_to_screen(make_result(Landmark(0.2, 0.0)))

    assert position == (79, 0)


def test_tracking_loss_briefly_returns_last_valid_position(monkeypatch):
    now = 10.0
    monkeypatch.setattr("gestures.cursor_mapper.time.time", lambda: now)
    mapper = CursorMapper(
        screen_width=100,
        screen_height=50,
        cursor_landmark_index=0,
        mouse_update_interval=0.0,
        deadzone_pixels=0,
        loss_hold_seconds=0.5,
    )

    assert mapper.map_to_screen(make_result(Landmark(0.0, 0.0))) == (0, 0)

    monkeypatch.setattr("gestures.cursor_mapper.time.time", lambda: now + 0.25)

    assert mapper.map_to_screen(None) == (0, 0)


def test_rate_limit_returns_none_before_update_interval(monkeypatch):
    times = iter([10.0, 10.01])
    monkeypatch.setattr("gestures.cursor_mapper.time.time", lambda: next(times))
    mapper = CursorMapper(
        screen_width=100,
        screen_height=50,
        cursor_landmark_index=0,
        mouse_update_interval=0.05,
        deadzone_pixels=0,
    )

    assert mapper.map_to_screen(make_result(Landmark(0.0, 0.0))) == (0, 0)
    assert mapper.map_to_screen(make_result(Landmark(1.0, 1.0))) is None
