import time
from collections import deque


class DynamicGestureDetector:
    """
    Detects movement-based gestures, such as swipes, by tracking
    the recent movement history of one hand landmark.

    This class does not execute actions.
    It only returns dynamic gesture names such as:
    - "SWIPE_LEFT"
    - "SWIPE_RIGHT"
    - "SWIPE_UP"
    - "SWIPE_DOWN"
    - None
    """

    def __init__(
        self,
        landmark_index: int = 8,
        history_size: int = 12,
        swipe_threshold: float = 0.25,
        max_swipe_time: float = 0.7,
        min_direction_ratio: float = 1.5,
        cooldown_seconds: float = 0.8,
    ):
        self.landmark_index = landmark_index
        self.history = deque(maxlen=history_size)

        # Required normalized movement amount.
        # Example: 0.25 means 25% of the camera frame width/height.
        self.swipe_threshold = swipe_threshold

        # Swipe must happen within this time window.
        self.max_swipe_time = max_swipe_time

        # Horizontal movement should dominate vertical movement,
        # or vertical movement should dominate horizontal movement.
        self.min_direction_ratio = min_direction_ratio

        # Prevent repeated swipe firing.
        self.cooldown_seconds = cooldown_seconds
        self.last_detection_time = 0.0

    def update(self, latest_result) -> str | None:
        """
        Updates the detector with the latest MediaPipe result.

        Returns:
            A dynamic gesture name, or None.
        """
        if latest_result is None or not latest_result.hand_landmarks:
            self.history.clear()
            return None

        hand_landmarks = latest_result.hand_landmarks[0]

        if len(hand_landmarks) <= self.landmark_index:
            self.history.clear()
            return None

        landmark = hand_landmarks[self.landmark_index]

        now = time.time()

        # Store normalized coordinates.
        self.history.append((now, landmark.x, landmark.y))

        if len(self.history) < 2:
            return None

        if now - self.last_detection_time < self.cooldown_seconds:
            return None

        dynamic_gesture = self._detect_swipe()

        if dynamic_gesture is not None:
            self.last_detection_time = now
            self.history.clear()

        return dynamic_gesture

    def _detect_swipe(self) -> str | None:
        start_time, start_x, start_y = self.history[0]
        end_time, end_x, end_y = self.history[-1]

        elapsed = end_time - start_time

        if elapsed <= 0:
            return None

        if elapsed > self.max_swipe_time:
            return None

        dx = end_x - start_x
        dy = end_y - start_y

        abs_dx = abs(dx)
        abs_dy = abs(dy)

        # Horizontal swipe
        if (
            abs_dx >= self.swipe_threshold
            and abs_dx >= abs_dy * self.min_direction_ratio
        ):
            if dx > 0:
                return "SWIPE_RIGHT"

            return "SWIPE_LEFT"

        # Vertical swipe
        if (
            abs_dy >= self.swipe_threshold
            and abs_dy >= abs_dx * self.min_direction_ratio
        ):
            if dy > 0:
                return "SWIPE_DOWN"

            return "SWIPE_UP"

        return None

    def reset(self) -> None:
        self.history.clear()
        self.last_detection_time = 0.0