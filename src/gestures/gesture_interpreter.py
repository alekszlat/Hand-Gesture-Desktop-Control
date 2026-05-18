class GestureInterpreter:
    def __init__(self, min_confidence: float = 0.5):
        self.gesture = "None"
        self.confidence = 0.0
        self.min_confidence = min_confidence

    def interpret_gesture(self, result) -> tuple[str, float]:
        if result is None:
            self.gesture = None
            self.confidence = 0.0
            return self.gesture, self.confidence

        if not result.gestures:
            self.gesture = None
            self.confidence = 0.0
            return self.gesture, self.confidence

        for hand_gestures in result.gestures:
            if not hand_gestures:
                continue

            top_gesture = hand_gestures[0]
            gesture_name = top_gesture.category_name
            confidence = top_gesture.score

            if confidence < self.min_confidence:
                self.gesture = None
                self.confidence = confidence
                return self.gesture, self.confidence

            self.gesture = gesture_name
            self.confidence = confidence
            return self.gesture, self.confidence

        self.gesture = None
        self.confidence = 0.0
        return self.gesture, self.confidence
        