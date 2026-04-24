class GestureInterpreter:
    def __init__(self):
        self.gesture = "None"

    def interpret_gesture(self, result):
        if result is None or not result.gestures:
            self.gesture = "None"
            return self.gesture

        for hand_gestures in result.gestures:
            if hand_gestures:
                top_gesture = hand_gestures[0]
                self.gesture = top_gesture.category_name
                return self.gesture
        