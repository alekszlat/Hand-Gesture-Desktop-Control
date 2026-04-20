import cv2 as cv

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

class FrameRenderer:
    def __init__(self, cursor_landmark_index=8):
        self.cursor_landmark_index = cursor_landmark_index  # Example: using the tip of the index finger as the cursor landmark

    def draw_hand_landmarks(self, frame, result):
        
        if result is None:
            return frame

        h, w, _ = frame.shape

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                points = []

                for i, lm in enumerate(hand_landmarks):
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    points.append((x, y))

                    color = (0, 255, 0)
                    if i == self.cursor_landmark_index:
                        color = (0, 0, 255)  # highlight landmark used for cursor

                    cv.circle(frame, (x, y), 5, color, -1)

                for start_idx, end_idx in HAND_CONNECTIONS:
                    if start_idx < len(points) and end_idx < len(points):
                        cv.line(frame, points[start_idx], points[end_idx], (255, 0, 0), 2)

        if result.gestures:
            for i, hand_gestures in enumerate(result.gestures):
                if hand_gestures:
                    top_gesture = hand_gestures[0]
                    label = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
                    cv.putText(
                        frame,
                        label,
                        (10, 30 + i * 30),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

        return frame