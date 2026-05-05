class GestureInterpreter:
    def __init__(self):
        self.gesture = "None"
        self.confidence = 0.0

    def interpret_gesture(self, result) -> tuple[str, float]:
        if result is None or not result.gestures:
            self.gesture = "None"
            self.confidence = 0.0
            return tuple((self.gesture, self.confidence))

        for hand_gestures in result.gestures:
            if hand_gestures:
                top_gesture = hand_gestures[0]
                self.gesture = top_gesture.category_name
                self.confidence = top_gesture.score
                return tuple((self.gesture, self.confidence))
        