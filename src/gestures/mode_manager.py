from enum import Enum

from gestures.gesture_state import GestureState


class AppMode(Enum):
    BASE = "BASE"
    DRAG = "DRAG"
    LAUNCHER = "LAUNCHER"
    COMMAND = "COMMAND"
    CONFIRM_CLOSE = "CONFIRM_CLOSE"


class ModeManager:
    """
    Tracks the current interaction mode of the app.

    It decides when the app should switch between modes such as:
    - BASE
    - DRAG
    - LAUNCHER
    - COMMAND
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
        dynamic_gesture: str | None = None,
    ) -> AppMode:
        if gesture_state is None:
            return self.current_mode

        # BASE mode transitions
        if self.current_mode == AppMode.BASE:
            self._update_from_base(gesture_state, dynamic_gesture)

        # DRAG mode transitions
        elif self.current_mode == AppMode.DRAG:
            self._update_from_drag(gesture_state, dynamic_gesture)

        # LAUNCHER mode transitions
        elif self.current_mode == AppMode.LAUNCHER:
            self._update_from_launcher(gesture_state, dynamic_gesture)

        # COMMAND mode transitions
        elif self.current_mode == AppMode.COMMAND:
            self._update_from_command(gesture_state, dynamic_gesture)

        # CONFIRM_CLOSE mode transitions
        elif self.current_mode == AppMode.CONFIRM_CLOSE:
            self._update_from_confirm_close(gesture_state, dynamic_gesture)

        return self.current_mode

    def _update_from_base(
        self,
        gesture_state: GestureState,
        dynamic_gesture: str | None,
    ) -> None:
        # Closed fist starts drag mode
        if gesture_state.changed_to("Closed_Fist"):
            self.current_mode = AppMode.DRAG
            return

        # Thumb up held enters launcher mode
        if gesture_state.is_gesture("Thumb_Up") and gesture_state.held_for(
            self.launcher_hold_seconds
        ):
            self.current_mode = AppMode.LAUNCHER
            return

        # Optional: Victory held enters command mode
        if gesture_state.is_gesture("Victory") and gesture_state.held_for(
            self.command_hold_seconds
        ):
            self.current_mode = AppMode.COMMAND
            return
        
        if gesture_state.is_gesture("ILoveYou") and gesture_state.held_for(
            self.confirm_close_hold_seconds
        ):
            self.current_mode = AppMode.CONFIRM_CLOSE
            return

    def _update_from_drag(
        self,
        gesture_state: GestureState,
        dynamic_gesture: str | None,
    ) -> None:
        # Open palm exits drag mode
        if gesture_state.changed_to("Open_Palm"):
            self.current_mode = AppMode.BASE
            return

        # If tracking is lost, exit drag mode for safety
        if gesture_state.name is None:
            self.current_mode = AppMode.BASE
            return

    def _update_from_launcher(
        self,
        gesture_state: GestureState,
        dynamic_gesture: str | None,
    ) -> None:
        # Closed fist cancels launcher
        if gesture_state.changed_to("Closed_Fist"):
            self.current_mode = AppMode.BASE
            return


    def _update_from_command(
        self,
        gesture_state: GestureState,
        dynamic_gesture: str | None,
    ) -> None:
        # Open palm exits command mode
        if gesture_state.changed_to("Open_Palm"):
            self.current_mode = AppMode.BASE
            return

        # Thumb up held enters close confirmation
        if gesture_state.is_gesture("Thumb_Up") and gesture_state.held_for(
            self.close_hold_seconds
        ):
            self.current_mode = AppMode.CONFIRM_CLOSE
            return

    def _update_from_confirm_close(
        self,
        gesture_state: GestureState,
        dynamic_gesture: str | None,
    ) -> None:
        # Open palm cancels close confirmation
        if gesture_state.changed_to("Open_Palm"):
            self.current_mode = AppMode.BASE
            return

        # Closed fist confirms close.
        #if gesture_state.changed_to("Closed_Fist"):
        #    self.current_mode = AppMode.BASE
        #    return

    def reset(self) -> AppMode:
        self.current_mode = AppMode.BASE
        return self.current_mode