import time


class CursorMapper:
    def __init__(
        self,
        screen_width,
        screen_height,
        cursor_landmark_index=8,
        mouse_update_interval=0.05,
        mirror_x=False,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_landmark_index = cursor_landmark_index
        self.mouse_update_interval = mouse_update_interval
        self.mirror_x = mirror_x

        self.last_mouse_update_time = 0.0
        self.last_mouse_position = None

    def map_to_screen(self, latest_result):
        now = time.time()
        if now - self.last_mouse_update_time < self.mouse_update_interval:
            return None

        if latest_result is None or not latest_result.hand_landmarks:
            return None

        hand_landmarks = latest_result.hand_landmarks[0]

        if len(hand_landmarks) <= self.cursor_landmark_index:
            return None

        landmark = hand_landmarks[self.cursor_landmark_index]

        screen_x = int(landmark.x * self.screen_width)
        screen_y = int(landmark.y * self.screen_height)

        if self.mirror_x:
            screen_x = self.screen_width - 1 - screen_x

        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))

        target_position = (screen_x, screen_y)

        if target_position == self.last_mouse_position:
            return None

        self.last_mouse_position = target_position
        self.last_mouse_update_time = now
        return target_position