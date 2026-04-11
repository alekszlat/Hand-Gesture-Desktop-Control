import time
import cv2 as cv
import mediapipe as mp
import subprocess

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


def mousemove(*, x, y, sync=False, execute=True):
    command = ["xdotool", "mousemove"]

    if sync:
        command.append("--sync")

    command.extend([str(x), str(y)])

    if execute:
        subprocess.call(command)

    return command


latest_result = None

# Screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Landmark used for cursor control: index fingertip
CURSOR_LANDMARK_INDEX = 9

# Rate limiting
MOUSE_UPDATE_INTERVAL = 0.05  # seconds
last_mouse_update_time = 0.0

# Prevent sending same position repeatedly
last_mouse_position = None

# Hand landmark connections
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]


def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path="./gesture_recognizer.task"),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    result_callback=print_result
)


def draw_hand_landmarks(frame, result):
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
                if i == CURSOR_LANDMARK_INDEX:
                    color = (0, 0, 255)  # highlight fingertip used for cursor

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


def move_mouse_from_landmark(result):
    global last_mouse_update_time, last_mouse_position

    if result is None or not result.hand_landmarks:
        return

    now = time.time()
    if now - last_mouse_update_time < MOUSE_UPDATE_INTERVAL:
        return

    # Use first detected hand
    hand_landmarks = result.hand_landmarks[0]

    if len(hand_landmarks) <= CURSOR_LANDMARK_INDEX:
        return

    landmark = hand_landmarks[CURSOR_LANDMARK_INDEX]

    # Convert normalized landmark coordinates to screen coordinates
    screen_x = int(landmark.x * SCREEN_WIDTH)
    screen_y = int(landmark.y * SCREEN_HEIGHT)

    target_position = (screen_x, screen_y)

    # Avoid sending duplicate mouse commands
    if target_position == last_mouse_position:
        return

    mousemove(x=screen_x, y=screen_y, sync=False)
    last_mouse_position = target_position
    last_mouse_update_time = now


def detect_gestures():
    cam = cv.VideoCapture(0)

    if not cam.isOpened():
        print("Could not open camera.")
        return

    with GestureRecognizer.create_from_options(options) as recognizer:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to read frame.")
                break

            frame = cv.flip(frame, 1)

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            timestamp_ms = int(time.time() * 1000)
            recognizer.recognize_async(mp_image, timestamp_ms)

            output_frame = frame.copy()
            draw_hand_landmarks(output_frame, latest_result)
            move_mouse_from_landmark(latest_result)

            cv.imshow("Gesture Detect", output_frame)

            if cv.waitKey(1) & 0xFF == 27:
                break

    cam.release()
    cv.destroyAllWindows()


def main():
    detect_gestures()


if __name__ == "__main__":
    main()