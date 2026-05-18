"""Gesture-to-action dispatch rules."""

import time

from gestures.mode_manager import AppMode


class ActionDispatcher:
    """Chooses when controllers should run actions for the current mode."""

    def __init__(
        self,
        mouse_controller,
        app_controller,
        window_controller,
        click_cooldown: float = 0.6,
        launcher_action_cooldown: float = 1.0,
        window_action_cooldown: float = 1.0,
    ):
        self.mouse_controller = mouse_controller
        self.app_controller = app_controller
        self.window_controller = window_controller

        self.click_cooldown = click_cooldown
        self.launcher_action_cooldown = launcher_action_cooldown
        self.window_action_cooldown = window_action_cooldown

        self.last_action_time = {}

    def dispatch(
        self,
        mode: AppMode,
        gesture_state,
        cursor_pos: tuple[int, int] | None = None,
    ) -> None:
        if gesture_state is None:
            return

        self._handle_cursor_movement(mode, cursor_pos)
        self._handle_mouse_actions(mode, gesture_state)
        self._handle_launcher_actions(mode, gesture_state)
        self._handle_window_actions(mode, gesture_state)

    def _handle_cursor_movement(
        self,
        mode: AppMode,
        cursor_pos: tuple[int, int] | None,
    ) -> None:
        if cursor_pos is None:
            return

        if mode in (AppMode.BASE, AppMode.DRAG):
            self.mouse_controller.movemouse(cursor_pos[0], cursor_pos[1])

    def _handle_mouse_actions(self, mode: AppMode, gesture_state) -> None:
        if (
            mode == AppMode.DRAG
            and gesture_state.name == "Closed_Fist"
            and not self.mouse_controller.is_grabbing
        ):
            self.mouse_controller.mousegrab()
            return

        if (
            self.mouse_controller.is_grabbing
            and gesture_state.name != "Closed_Fist"
            and gesture_state.changed_to("Open_Palm")
        ):
            self.mouse_controller.mouserelease()
            return

        if (
            mode == AppMode.BASE
            and gesture_state.changed_to("Pointing_Up")
            and self._can_fire("click", self.click_cooldown)
        ):
            self.mouse_controller.mouseclick(button=1)
            return

    def _handle_launcher_actions(self, mode: AppMode, gesture_state) -> None:
        if mode != AppMode.LAUNCHER:
            return

        if gesture_state.changed_to("ILoveYou") and self._can_fire(
            "open_browser", self.launcher_action_cooldown
        ):
            self.app_controller.open_browser()
            return

        if gesture_state.changed_to("Pointing_Up") and self._can_fire(
            "open_discord", self.launcher_action_cooldown
        ):
            self.app_controller.open_discord()
            return

        if gesture_state.changed_to("Victory") and self._can_fire(
            "open_vscode", self.launcher_action_cooldown
        ):
            self.app_controller.open_vscode()
            return

    def _handle_window_actions(
        self,
        mode: AppMode,
        gesture_state,
    ) -> None:
        if (
            mode == AppMode.CONFIRM_CLOSE
            and gesture_state.changed_to("Pointing_Up")
            and self._can_fire("close_active_window", self.window_action_cooldown)
        ):
            self.window_controller.close_active_window()
            return

        if (
            mode == AppMode.CONFIRM_CLOSE
            and gesture_state.changed_to("Closed_Fist")
            and self._can_fire("close_app", self.window_action_cooldown)
        ):
            self.window_controller.close_app()
            return

    def _can_fire(self, action_name: str, cooldown: float) -> bool:
        now = time.time()
        last_time = self.last_action_time.get(action_name, 0.0)

        if now - last_time < cooldown:
            return False

        self.last_action_time[action_name] = now
        return True
