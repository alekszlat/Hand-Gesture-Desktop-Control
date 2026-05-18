from enum import Enum

from gestures.gesture_state import GestureState

import numpy as np
import sounddevice as sd

class AppMode(Enum):
    BASE = "BASE"
    DRAG = "DRAG"
    LAUNCHER = "LAUNCHER"
    CONFIRM_CLOSE = "CONFIRM_CLOSE"


class ModeManager:
    """
    Tracks the current interaction mode of the app.

    It decides when the app should switch between modes such as:
    - BASE
    - DRAG
    - LAUNCHER
    - CONFIRM_CLOSE
    """

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

        # BASE mode transitions
        if self.current_mode == AppMode.BASE:
            self._update_from_base(gesture_state)

        # DRAG mode transitions
        elif self.current_mode == AppMode.DRAG:
            self._update_from_drag(gesture_state)

        # LAUNCHER mode transitions
        elif self.current_mode == AppMode.LAUNCHER:
            self._update_from_launcher(gesture_state)

        # CONFIRM_CLOSE mode transitions
        elif self.current_mode == AppMode.CONFIRM_CLOSE:
            self._update_from_confirm_close(gesture_state)
        return self.current_mode

    def _update_from_base(
        self,
        gesture_state: GestureState,
    ) -> None:
        
        # Closed fist starts drag mode
        if gesture_state.changed_to("Closed_Fist"):
            self.current_mode = AppMode.DRAG
            return

        # Thumb up held enters launcher mode
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
        
        # Open palm exits drag mode
        if gesture_state.changed_to("Open_Palm") or gesture_state.changed_to("Unknown"):  # If tracking is lost, exit drag mode for safety
            self.current_mode = AppMode.BASE
            return

    def _update_from_launcher(
        self,
        gesture_state: GestureState,
    ) -> None:
        # Closed fist cancels launcher
        if gesture_state.changed_to("Closed_Fist"):
            self._play_mode_change_sound()
            self.current_mode = AppMode.BASE
            return

    def _update_from_confirm_close(
        self,
        gesture_state: GestureState,
    ) -> None:
        # Thumb_Up cancels close confirmation
        if gesture_state.changed_to("Thumb_Up"):
            self._play_mode_change_sound()
            self.current_mode = AppMode.BASE
            return

    def reset(self) -> AppMode:
        self.current_mode = AppMode.BASE
        return self.current_mode
    
    # For debugging purposes, sound an alert when you change modes
    def _play_mode_change_sound(self):
        # Generate a 440 Hz sine wave for 0.1 seconds
        fs = 44100  # Sample rate
        duration = 0.1  # Duration in seconds
        frequency = 440  # Frequency in Hz (A4 note)
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)

        # Play the sound
        sd.play(audio_data, fs)