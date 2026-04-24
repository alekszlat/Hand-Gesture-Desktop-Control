import cv2 as cv

import camera.CameraStream as CameraStream
import tracking.HandTracker as HandTracker
import debugging.FrameRenderer as FrameRenderer
import gestures.CursorMapper as CursorMapper
import control.MouseController as MouseController
import gestures.GestureInterpreter as GestureInterpreter
import control.ActionDispatcher as ActionDispatcher


class App:
    def __init__(
        self,
        screen_width=1920,
        screen_height=1080,
        cursor_landmark_index=5,
        model_path="models/gesture_recognizer.task",
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cursor_landmark_index = cursor_landmark_index
        self.model_path = model_path

        self.cam = CameraStream.CameraStream()
        self.hand_tracker = HandTracker.HandTracker(model_path=self.model_path)
        self.cursor_mapper = CursorMapper.CursorMapper(
            self.screen_width,
            self.screen_height,
            self.cursor_landmark_index,
        )
        self.gesture_interpreter = GestureInterpreter.GestureInterpreter()
        self.mouse_controller = MouseController.MouseController()
        self.action_dispatcher = ActionDispatcher.ActionDispatcher()
        self.frame_renderer = FrameRenderer.FrameRenderer(self.cursor_landmark_index)

        self.window_name = "Gesture Detect"
        self.running = False

    def run(self):
        self.running = True

        try:
            while self.running:
                self.update()

                if cv.waitKey(1) & 0xFF == 27:
                    self.running = False

        except Exception as e:
            print(f"Error in app loop: {e}")

        finally:
            self.shutdown()

    def update(self):
        frame = self.cam.read_frame()

        # Send frame to tracker
        pros_frame=self.hand_tracker.process_frame(frame)
        latest_result = self.hand_tracker.get_latest_result()

        # Prepare output frame
        output_frame = pros_frame.copy()

        # Map cursor position
        mouse_pos = self.cursor_mapper.map_to_screen(latest_result)
        if mouse_pos is not None:
            self.mouse_controller.movemouse(mouse_pos[0], mouse_pos[1])

        # Interpret gesture
        gesture = self.gesture_interpreter.interpret_gesture(latest_result)

        # Dispatch action
        self.action_dispatcher.dispatch(gesture)

        # Draw landmarks and gesture info
        output_frame = self.frame_renderer.draw_hand_landmarks(output_frame, latest_result)
        output_frame = self.frame_renderer.draw_gesture_label(output_frame, gesture)

        cv.imshow(self.window_name, output_frame)

    def shutdown(self):
        self.cam.release()
        self.hand_tracker.close()
        cv.destroyAllWindows()


def main():
    app = App(
        screen_width=1920,
        screen_height=1080,
        cursor_landmark_index=5,
        model_path="models/gesture_recognizer.task",
    )
    app.run()


if __name__ == "__main__":
    main()