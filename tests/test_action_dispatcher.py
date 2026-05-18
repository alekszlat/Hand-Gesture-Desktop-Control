"""Tests for gesture-to-action dispatch without desktop automation."""

from control.action_dispatcher import ActionDispatcher
from gestures.gesture_state import GestureState
from gestures.mode_manager import AppMode


class FakeMouseController:
    def __init__(self):
        self.calls = []
        self.is_grabbing = False

    def movemouse(self, x, y):
        self.calls.append(("move", x, y))

    def mouseclick(self, button=1):
        self.calls.append(("click", button))

    def mousegrab(self):
        self.is_grabbing = True
        self.calls.append(("grab",))

    def mouserelease(self):
        self.is_grabbing = False
        self.calls.append(("release",))


class FakeAppController:
    def __init__(self):
        self.calls = []

    def open_browser(self):
        self.calls.append("browser")

    def open_vscode(self):
        self.calls.append("vscode")

    def open_discord(self):
        self.calls.append("discord")


class FakeWindowController:
    def __init__(self):
        self.calls = []

    def close_active_window(self):
        self.calls.append("close_window")

    def close_app(self):
        self.calls.append("close_app")


def make_dispatcher():
    mouse = FakeMouseController()
    apps = FakeAppController()
    windows = FakeWindowController()
    dispatcher = ActionDispatcher(
        mouse_controller=mouse,
        app_controller=apps,
        window_controller=windows,
        click_cooldown=0.0,
        launcher_action_cooldown=0.0,
        window_action_cooldown=0.0,
    )
    return dispatcher, mouse, apps, windows


def state(name, previous_name=None, changed=True):
    return GestureState(
        name=name,
        previous_name=previous_name,
        confidence=1.0,
        duration=0.0,
        changed=changed,
    )


def test_base_mode_moves_cursor_and_clicks_on_pointing_up():
    dispatcher, mouse, apps, windows = make_dispatcher()

    dispatcher.dispatch(
        mode=AppMode.BASE,
        gesture_state=state("Pointing_Up", previous_name=None),
        cursor_pos=(120, 240),
    )

    assert mouse.calls == [("move", 120, 240), ("click", 1)]
    assert apps.calls == []
    assert windows.calls == []


def test_launcher_mode_maps_gestures_to_app_launches():
    dispatcher, mouse, apps, windows = make_dispatcher()

    dispatcher.dispatch(AppMode.LAUNCHER, state("ILoveYou", previous_name="Thumb_Up"))
    dispatcher.dispatch(
        AppMode.LAUNCHER, state("Pointing_Up", previous_name="ILoveYou")
    )
    dispatcher.dispatch(AppMode.LAUNCHER, state("Victory", previous_name="Pointing_Up"))

    assert apps.calls == ["browser", "discord", "vscode"]
    assert mouse.calls == []
    assert windows.calls == []


def test_drag_mode_grabs_and_releases_mouse():
    dispatcher, mouse, _, _ = make_dispatcher()

    dispatcher.dispatch(AppMode.DRAG, state("Closed_Fist", previous_name="Open_Palm"))
    dispatcher.dispatch(AppMode.DRAG, state("Open_Palm", previous_name="Closed_Fist"))

    assert mouse.calls == [("grab",), ("release",)]
    assert mouse.is_grabbing is False


def test_confirm_close_mode_dispatches_window_actions():
    dispatcher, _, _, windows = make_dispatcher()

    dispatcher.dispatch(
        AppMode.CONFIRM_CLOSE,
        state("Pointing_Up", previous_name="ILoveYou"),
    )
    dispatcher.dispatch(
        AppMode.CONFIRM_CLOSE,
        state("Closed_Fist", previous_name="Pointing_Up"),
    )

    assert windows.calls == ["close_window", "close_app"]
