"""Tests for mode transitions without playing audio."""

import builtins

from gestures.gesture_state import GestureState
from gestures.mode_manager import AppMode, ModeManager


def state(name, previous_name=None, duration=0.0, changed=True):
    return GestureState(
        name=name,
        previous_name=previous_name,
        confidence=1.0,
        duration=duration,
        changed=changed,
    )


def test_closed_fist_enters_drag_mode():
    manager = ModeManager()

    mode = manager.update(state("Closed_Fist", previous_name="Open_Palm"))

    assert mode == AppMode.DRAG


def test_open_palm_exits_drag_mode():
    manager = ModeManager()
    manager.current_mode = AppMode.DRAG

    mode = manager.update(state("Open_Palm", previous_name="Closed_Fist"))

    assert mode == AppMode.BASE


def test_thumb_up_hold_enters_launcher_mode(monkeypatch):
    manager = ModeManager(launcher_hold_seconds=1.0)
    monkeypatch.setattr(manager, "_play_mode_change_sound", lambda: None)

    mode = manager.update(state("Thumb_Up", duration=1.2, changed=False))

    assert mode == AppMode.LAUNCHER


def test_confirm_close_mode_can_be_cancelled(monkeypatch):
    manager = ModeManager()
    manager.current_mode = AppMode.CONFIRM_CLOSE
    monkeypatch.setattr(manager, "_play_mode_change_sound", lambda: None)

    mode = manager.update(state("Thumb_Up", previous_name="ILoveYou"))

    assert mode == AppMode.BASE


def test_mode_change_sound_is_optional_when_portaudio_is_missing(monkeypatch):
    manager = ModeManager()
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "sounddevice":
            raise OSError("PortAudio library not found")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    manager._play_mode_change_sound()
