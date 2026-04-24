import time


class CursorMapper:
    def __init__(
        self,
        screen_width,
        screen_height,
        cursor_landmark_index=8,
        mouse_update_interval=0.01,
        mirror_x=False,
        landmark_smoothing=0.18,
        deadzone_pixels=6,
        loss_hold_seconds=0.20,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_landmark_index = cursor_landmark_index
        self.mouse_update_interval = mouse_update_interval
        self.mirror_x = mirror_x

        # Smaller = smoother, but slower response
        self.landmark_smoothing = landmark_smoothing

        # Ignore very tiny cursor motion
        self.deadzone_pixels = deadzone_pixels

        # Keep last valid cursor briefly if tracking disappears
        self.loss_hold_seconds = loss_hold_seconds

        self.last_mouse_update_time = 0.0
        self.last_mouse_position = None
        self.last_valid_tracking_time = 0.0

        # Smoothed normalized landmark coordinates
        self.smoothed_landmark_x = None
        self.smoothed_landmark_y = None

    def map_to_screen(self, latest_result):
        now = time.time()

        if now - self.last_mouse_update_time < self.mouse_update_interval:
            return None

        if latest_result is None or not latest_result.hand_landmarks:
            return self._handle_tracking_loss(now)

        hand_landmarks = latest_result.hand_landmarks[0]

        if len(hand_landmarks) <= self.cursor_landmark_index:
            return self._handle_tracking_loss(now)

        landmark = hand_landmarks[self.cursor_landmark_index]

        # Clamp normalized coordinates first
        raw_x = max(0.0, min(landmark.x, 1.0))
        raw_y = max(0.0, min(landmark.y, 1.0))

        # Smooth landmark coordinates before mapping to screen
        if self.smoothed_landmark_x is None or self.smoothed_landmark_y is None:
            self.smoothed_landmark_x = raw_x
            self.smoothed_landmark_y = raw_y
        else:
            alpha = self.landmark_smoothing
            self.smoothed_landmark_x = alpha * raw_x + (1.0 - alpha) * self.smoothed_landmark_x
            self.smoothed_landmark_y = alpha * raw_y + (1.0 - alpha) * self.smoothed_landmark_y

        norm_x = self.smoothed_landmark_x
        norm_y = self.smoothed_landmark_y

        if self.mirror_x:
            norm_x = 1.0 - norm_x

        screen_x = int(round(norm_x * (self.screen_width - 1)))
        screen_y = int(round(norm_y * (self.screen_height - 1)))

        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))

        target_position = (screen_x, screen_y)

        if self.last_mouse_position is not None:
            dx = abs(target_position[0] - self.last_mouse_position[0])
            dy = abs(target_position[1] - self.last_mouse_position[1])

            if dx < self.deadzone_pixels and dy < self.deadzone_pixels:
                return None

        self.last_mouse_position = target_position
        self.last_valid_tracking_time = now
        self.last_mouse_update_time = now
        return target_position

    def _handle_tracking_loss(self, now):
        if (
            self.last_mouse_position is not None
            and now - self.last_valid_tracking_time <= self.loss_hold_seconds
        ):
            self.last_mouse_update_time = now
            return self.last_mouse_position

        return None