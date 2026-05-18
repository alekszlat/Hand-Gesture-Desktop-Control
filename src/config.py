"""Typed runtime settings shared by the app, UI, and controllers."""

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parent / "models" / "gesture_recognizer.task"
)


@dataclass
class CameraConfig:
    camera_index: int = 0


@dataclass
class TrackingConfig:
    model_path: str = str(DEFAULT_MODEL_PATH)
    num_hands: int = 1
    min_detection_confidence: float = 0.35
    min_presence_confidence: float = 0.35
    min_tracking_confidence: float = 0.35


@dataclass
class GestureConfig:
    min_confidence: float = 0.5


@dataclass
class CursorConfig:
    screen_width: int = 1920
    screen_height: int = 1080
    cursor_landmark_index: int = 5
    mouse_update_interval: float = 0.01
    mirror_x: bool = False
    landmark_smoothing: float = 0.18
    deadzone_pixels: int = 6
    loss_hold_seconds: float = 0.20


@dataclass
class ActionConfig:
    click_cooldown: float = 0.6
    launcher_action_cooldown: float = 1.0
    window_action_cooldown: float = 1.0


@dataclass
class UiConfig:
    show_status_widget: bool = True


@dataclass
class AppConfig:
    """Top-level settings object passed into App at startup."""

    window_name: str = "Gesture Detect"
    camera: CameraConfig = field(default_factory=CameraConfig)
    tracking: TrackingConfig = field(default_factory=TrackingConfig)
    gesture: GestureConfig = field(default_factory=GestureConfig)
    cursor: CursorConfig = field(default_factory=CursorConfig)
    actions: ActionConfig = field(default_factory=ActionConfig)
    ui: UiConfig = field(default_factory=UiConfig)
