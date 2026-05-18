"""Gesture-driven interaction mode state machine."""

from enum import Enum

import numpy as np

from gestures.gesture_state import GestureState


class AppMode(Enum):
    """High-level interaction modes used by the dispatcher and UI."""

    BASE = "BASE"
    DRAG = "DRAG"
    LAUNCHER = "LAUNCHER"
    CONFIRM_CLOSE = "CONFIRM_CLOSE"


class ModeManager:
    """Updates the current interaction mode from gesture state."""

    def __init__(
        self,
        launcher_hold_seconds: float = 1.0,
        close_hold_seconds: float = 2.0,
        command_hold_seconds: float = 1.2,
        confirm_close_hold_seconds: float = 1.5,
    ):
        self.current_mode = AppMode.BASE

        self.launcher_hold_seconds = launcher_hold_seconds
        self.close_hold_seconds = close_hold_seconds
        self.command_hold_seconds = command_hold_seconds
        self.confirm_close_hold_seconds = confirm_close_hold_seconds

    def update(
        self,
        gesture_state: GestureState,
    ) -> AppMode:
        if gesture_state is None:
            return self.current_mode

        if self.current_mode == AppMode.BASE:
            self._update_from_base(gesture_state)

        elif self.current_mode == AppMode.DRAG:
            self._update_from_drag(gesture_state)

        elif self.current_mode == AppMode.LAUNCHER:
            self._update_from_launcher(gesture_state)

        elif self.current_mode == AppMode.CONFIRM_CLOSE:
            self._update_from_confirm_close(gesture_state)
        return self.current_mode

    def _update_from_base(
        self,
        gesture_state: GestureState,
    ) -> None:
        if gesture_state.changed_to("Closed_Fist"):
            self.current_mode = AppMode.DRAG
            return

        if gesture_state.is_gesture("Thumb_Up") and gesture_state.held_for(
            self.launcher_hold_seconds
        ):
            self._play_mode_change_sound()
            self.current_mode = AppMode.LAUNCHER
            return

        if gesture_state.is_gesture("ILoveYou") and gesture_state.held_for(
            self.confirm_close_hold_seconds
        ):
            self._play_mode_change_sound()
            self.current_mode = AppMode.CONFIRM_CLOSE
            return

    def _update_from_drag(
        self,
        gesture_state: GestureState,
    ) -> None:
        if gesture_state.changed_to("Open_Palm") or gesture_state.changed_to("Unknown"):
            self.current_mode = AppMode.BASE
            return

    def _update_from_launcher(
        self,
        gesture_state: GestureState,
    ) -> None:
        if gesture_state.changed_to("Closed_Fist"):
            self._play_mode_change_sound()
            self.current_mode = AppMode.BASE
            return

    def _update_from_confirm_close(
        self,
        gesture_state: GestureState,
    ) -> None:
        if gesture_state.changed_to("Thumb_Up"):
            self._play_mode_change_sound()
            self.current_mode = AppMode.BASE
            return

    def reset(self) -> AppMode:
        self.current_mode = AppMode.BASE
        return self.current_mode

    def _play_mode_change_sound(self):
        """Play a short feedback tone when the mode changes."""

        try:
            import sounddevice as sd
        except OSError:
            return

        fs = 44100
        duration = 0.1
        frequency = 440
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

        sd.play(audio_data, fs)
