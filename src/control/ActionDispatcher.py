import control.MouseController as MouseController

class ActionDispatcher:
    def __init__(self):
        self.mouse_controller = MouseController.MouseController()
        self.gesture_action_map = {
            "Open_Palm": {"type": "release"},
            "Closed_Fist": {"type": "grab", "button": 1},
            "Pointing_Up": {"type": "click", "button": 3},
            "Thumb_Up": {"type": "press_Esc"},
        }

    def dispatch(self, gesture):
        if gesture is None or gesture == "None":
            return

        type_action = self.gesture_action_map.get(gesture)
        if type_action is None:
            return

        if type_action["type"] == "grab":
            self.mouse_controller.mousegrab()
        elif type_action["type"] == "release":
            self.mouse_controller.mouserelease()
        elif type_action["type"] == "click":
            self.mouse_controller.mouseclick(type_action["button"])
        elif type_action["type"] == "press_Esc":
            self.mouse_controller.press_Esc()
        