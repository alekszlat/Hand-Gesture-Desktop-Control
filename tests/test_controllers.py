"""Tests for controller command construction without executing commands."""

from control.mouse_controller import MouseController
from control.window_controller import WindowController


def test_mouse_controller_builds_xdotool_commands_without_execution():
    mouse = MouseController()

    assert mouse.movemouse(10, 20, sync=True, execute=False) == [
        "xdotool",
        "mousemove",
        "--sync",
        "10",
        "20",
    ]
    assert mouse.mouseclick(button=3, execute=False) == ["xdotool", "click", "3"]
    assert mouse.mousegrab(execute=False) == ["xdotool", "mousedown", "1"]
    assert mouse.is_grabbing is True
    assert mouse.mouserelease(execute=False) == ["xdotool", "mouseup", "1"]
    assert mouse.is_grabbing is False


def test_window_controller_uses_expected_fixed_monitor_positions(monkeypatch):
    controller = WindowController()
    calls = []

    monkeypatch.setattr(
        controller, "move_active_window", lambda x, y: calls.append((x, y))
    )

    controller.move_window_to_next_monitor()
    controller.move_window_to_previous_monitor()

    assert calls == [(1920, 100), (100, 100)]
