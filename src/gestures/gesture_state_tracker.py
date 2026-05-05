import time

from gestures.gesture_state import GestureState


class GestureStateTracker:
    """
    Tracks the current gesture over time.

    It detects:
    - current gesture name
    - previous gesture name
    - confidence
    - how long the current gesture has been held
    - whether the gesture changed on this update
    """

    def __init__(self):
        self.current_name: str | None = None
        self.previous_name: str | None = None
        self.current_confidence: float = 0.0
        self.gesture_start_time: float = time.time()

    def update(self, new_name: str | None, confidence: float = 0.0) -> GestureState:
        now = time.time()

        changed = new_name != self.current_name

        if changed:
            self.previous_name = self.current_name
            self.current_name = new_name
            self.current_confidence = confidence
            self.gesture_start_time = now
        else:
            self.current_confidence = confidence

        duration = now - self.gesture_start_time

        return GestureState(
            name=self.current_name,
            previous_name=self.previous_name,
            confidence=self.current_confidence,
            duration=duration,
            changed=changed,
        )

    def reset(self) -> GestureState:
        self.current_name = None
        self.previous_name = None
        self.current_confidence = 0.0
        self.gesture_start_time = time.time()

        return GestureState(
            name=None,
            previous_name=None,
            confidence=0.0,
            duration=0.0,
            changed=True,
        )