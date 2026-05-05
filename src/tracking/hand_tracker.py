import time
import cv2 as cv
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class HandTracker:
    def __init__(
            self, 
            model_path: str, 
            num_hands: int = 1, 
            min_detection_confidence: float = 0.35, 
            min_presence_confidence: float = 0.70,
            min_tracking_confidence: float = 0.35,):
        self.latest_result = None

        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
            result_callback=self._on_result,
        )

        self.recognizer = GestureRecognizer.create_from_options(self.options)

    def _on_result(
        self,
        result,
        output_image: mp.Image,
        timestamp_ms: int,
    ) -> None:
        self.latest_result = result

    def process_frame(self, iframe):
        frame = cv.flip(iframe, 1)  # Flip horizontally for a mirror effect
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int(time.time() * 1000)
        self.recognizer.recognize_async(mp_image, timestamp_ms)
        return frame

    def get_latest_result(self):
        return self.latest_result

    def close(self):
        if self.recognizer is not None:
            self.recognizer.close()
            self.recognizer = None